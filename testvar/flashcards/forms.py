from django import forms
from .models import Rating, Flashcard

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Leave a comment...'}),
        }


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['question', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter the question...'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter the answer...'}),
        }