from django.urls import path
from .views import ContestantCRUDView

urlpatterns = [
    path('all/', ContestantCRUDView.as_view()),  # For listing and creating
    path('<int:uid>/', ContestantCRUDView.as_view()),  # For retrieving, updating, and deleting
]
