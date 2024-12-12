from django.contrib import admin
from .models import FlashcardSet, Flashcard, Rating

# Register your models here.
admin.site.register(FlashcardSet)
admin.site.register(Flashcard)
admin.site.register(Rating)