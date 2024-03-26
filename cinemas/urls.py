from django.urls import path
from .views import (
    CinemaCreateView, 
    CinemaUpdateView, 
    CinemaDeleteView
)

urlpatterns = [
    path('add/', CinemaCreateView.as_view(), name='cinema_add'),
    path('<int:pk>/edit/', CinemaUpdateView.as_view(), name='cinema_edit'),
    path('<int:pk>/delete/', CinemaDeleteView.as_view(), name='cinema_delete'),
]
