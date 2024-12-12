from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import FlashcardSet, Flashcard, Rating
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RatingForm, FlashcardForm


def list_flashcard_sets(request):
    sets = FlashcardSet.objects.all()
    return render(request, 'flashcards/list.html', {'sets': sets})

@login_required  # Ensure only logged-in users can access this view
def create_flashcard_set(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        flashcard_set = FlashcardSet.objects.create(user=request.user, title=title, description=description)
        return redirect('flashcard_set_created', set_id=flashcard_set.id)
    
    return render(request, 'flashcards/create.html')

def study_flashcard_set(request, set_id):
    # Get the flashcard set and related flashcards
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()  # Get all flashcards for this set
    ratings = flashcard_set.ratings.all()  # Get all ratings for this set

    # Handle review (rating) submission
    if request.method == "POST":
        review_form = RatingForm(request.POST)
        if review_form.is_valid():
            # Check if a review already exists for this set and user
            existing_review = Rating.objects.filter(set=flashcard_set, user=request.user).first()
            if existing_review:
                # If a review already exists, update it
                existing_review.stars = review_form.cleaned_data['stars']
                existing_review.comment = review_form.cleaned_data['comment']
                existing_review.save()
            else:
                # If no review exists, create a new one
                review = review_form.save(commit=False)
                review.set = flashcard_set  # Associate the review with the current flashcard set
                review.user = request.user   # Associate the review with the logged-in user
                review.save()  # Save the review
            return redirect('study_flashcard_set', set_id=set_id)  # Redirect to the same page to display new review
        
        # Handle flashcard creation (this part is unchanged)
        form = FlashcardForm(request.POST)
        if form.is_valid():
            new_flashcard = form.save(commit=False)
            new_flashcard.set = flashcard_set  # Associate the flashcard with the current set
            new_flashcard.created_by = request.user  # Associate the flashcard with the current user
            new_flashcard.save()  # Save the new flashcard
            return redirect('study_flashcard_set', set_id=set_id)  # Redirect to the study page to display the new flashcard

    else:
        # Initialize the forms if it's a GET request
        review_form = RatingForm()
        form = FlashcardForm()

    # Render the page with flashcard set, flashcards, ratings, and forms
    return render(request, 'flashcards/study.html', {
        'flashcard_set': flashcard_set,
        'form': form,  # Flashcard creation form
        'review_form': review_form,  # Review form for rating
        'flashcards': flashcards,
        'ratings': ratings,
    })

def flashcard_set_created(request, set_id):
    # Get the newly created flashcard set by ID
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    
    return render(request, 'flashcards/flashcard_set_created.html', {'set_id': flashcard_set.id})

# View for editing a flashcard
def edit_flashcard(request, set_id, flashcard_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, set=flashcard_set)

    if request.user != flashcard.created_by:
        # Handle permission error, redirect or show an error message
        return redirect('study_flashcard_set', set_id=set_id)

    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('study_flashcard_set', set_id=set_id)
    else:
        form = FlashcardForm(instance=flashcard)

    return render(request, 'flashcards/edit_flashcard.html', {
        'form': form, 'flashcard_set': flashcard_set, 'flashcard': flashcard
    })

# View for deleting a flashcard
def delete_flashcard(request, set_id, flashcard_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, set=flashcard_set)

    if request.user != flashcard.created_by:
        # Handle permission error, redirect or show an error message
        return redirect('study_flashcard_set', set_id=set_id)

    flashcard.delete()
    return redirect('study_flashcard_set', set_id=set_id)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_flashcard_sets')  # Redirect to the list page after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and log them in automatically
            user = form.save()
            login(request, user)
            return redirect('list_flashcard_sets')  # Redirect to flashcard sets list after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})