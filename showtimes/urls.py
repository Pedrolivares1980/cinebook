from django.urls import path
from .views import ShowtimeListView, ShowtimeCreateView, ShowtimeUpdateView, ShowtimeDeleteView

urlpatterns = [
    path('', ShowtimeListView.as_view(), name='showtime_list'),
    path('create/', ShowtimeCreateView.as_view(), name='showtime_create'),
    path('update/<int:pk>/', ShowtimeUpdateView.as_view(), name='showtime_update'),
    path('delete/<int:pk>/', ShowtimeDeleteView.as_view(), name='showtime_delete'),
]