from django.urls import path
from .views import (
    ScreeningRoomCreateView, 
    ScreeningRoomUpdateView, 
    ScreeningRoomDeleteView
)

urlpatterns = [
    path('add/', ScreeningRoomCreateView.as_view(), name='screeningroom_create'), 
    path('<int:pk>/edit/', ScreeningRoomUpdateView.as_view(), name='screeningroom_update'), 
    path('<int:pk>/delete/', ScreeningRoomDeleteView.as_view(), name='screeningroom_delete'),  
    ]
