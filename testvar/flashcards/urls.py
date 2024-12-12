from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.list_flashcard_sets, name='list_flashcard_sets'),
    path('', views.list_flashcard_sets, name='home'),
    path('create/', views.create_flashcard_set, name='create_flashcard_set'),
    path('study/<int:set_id>/', views.study_flashcard_set, name='study_flashcard_set'),
    path('created/<int:set_id>/', views.flashcard_set_created, name='flashcard_set_created'),
    path('edit/<int:set_id>/<int:flashcard_id>/', views.edit_flashcard, name='edit_flashcard'),
    path('delete/<int:set_id>/<int:flashcard_id>/', views.delete_flashcard, name='delete_flashcard'),
]
