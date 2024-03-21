from django.urls import path
from .views import (
    ScreeningRoomListView, 
    ScreeningRoomCreateView, 
    ScreeningRoomUpdateView, 
    ScreeningRoomDeleteView
)

urlpatterns = [
    path('', ScreeningRoomListView.as_view(), name='screeningroom_list'),
    path('add/', ScreeningRoomCreateView.as_view(), name='screeningroom_create'), 
    path('<int:pk>/edit/', ScreeningRoomUpdateView.as_view(), name='screeningroom_update'), 
    path('<int:pk>/delete/', ScreeningRoomDeleteView.as_view(), name='screeningroom_delete'),  ]
