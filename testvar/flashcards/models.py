from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FlashcardSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        # Get all ratings for this flashcard set
        ratings = self.ratings.all()
        if ratings:
            # Calculate the average rating
            return sum([rating.stars for rating in ratings]) / len(ratings)
        return None  # If there are no ratings, return None or 0

class Flashcard(models.Model):
    set = models.ForeignKey(FlashcardSet, related_name="flashcards", on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return self.question

class Rating(models.Model):
    set = models.ForeignKey(FlashcardSet, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('set', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.set.title} - {self.stars} stars"
