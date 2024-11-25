from django.urls import path
from .views import VoteCRUDView

urlpatterns = [
    path('all/', VoteCRUDView.as_view()),  # List all votes or create a new vote
    path('<str:ip>/', VoteCRUDView.as_view()),  # Retrieve or delete a specific vote by IP
]
