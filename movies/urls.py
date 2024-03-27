from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('admin/create/', views.AdminMovieCreateView.as_view(), name='admin_movie_create'),
    path('admin/delete/<int:pk>/', views.AdminMovieDeleteView.as_view(), name='admin_movie_delete'),
    path('movies/suggestions/', views.movie_suggestions, name='movie_suggestions'),
]
