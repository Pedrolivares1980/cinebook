from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Movie
from showtimes.models import Showtime
from .forms import MovieForm
from django.http import JsonResponse
import requests
from django.conf import settings

def movie_suggestions(request):
    """
    Fetches movie suggestions from TMDB API based on the user's query.
    Returns a list of suggested movies in JSON format.
    """
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'results': []})

    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}"
    response = requests.get(search_url)
    if response.status_code == 200:
        search_results = response.json().get('results', [])
        simplified_results = [{'id': result['id'], 'title': result['title']} for result in search_results]
        return JsonResponse({'results': simplified_results})
    else:
        return JsonResponse({'error': 'Failed to fetch suggestions'}, status=response.status_code)

class MovieListView(ListView):
    """
    Displays a list of movies stored in the database.
    """
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'

    def get_queryset(self):
        """
        Override the default queryset to return random movies.
        """
        # Request the database to return random movies
        return Movie.objects.order_by('?')[:8]

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        showtimes = Showtime.objects.filter(movie=movie).select_related('screening_room__cinema')
        context['showtimes'] = showtimes
        return context

class AdminMovieCreateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'movies/admin_movies.html'

    def test_func(self):
        """Ensure only staff or superuser can access this view."""
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MovieForm()
        return context

    def post(self, request, *args, **kwargs):
        form = MovieForm(request.POST)
        if form.is_valid():
            tmdb_id = form.cleaned_data['tmdb_id']
            movie_data = self.fetch_movie_data_from_tmdb(tmdb_id)
            if movie_data:
                movie = self.create_movie_instance_from_tmdb_data(movie_data)
                if movie:
                    movie.save()
                    messages.success(request, 'Movie added successfully.')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Failed to create movie instance from TMDB data.')
            else:
                messages.error(request, 'Failed to fetch movie data from TMDB.')
        else:
            messages.error(request, 'Form is not valid.')

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MovieForm(request.POST)
        if form.is_valid():
            tmdb_id = form.cleaned_data['tmdb_id']
            movie_data = self.fetch_movie_data_from_tmdb(tmdb_id)
            if movie_data:
                movie = self.create_movie_instance_from_tmdb_data(movie_data)
                if movie:
                    movie.save()
                    messages.success(request, 'Movie added successfully.')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Failed to create movie instance from TMDB data.')
            else:
                messages.error(request, 'Failed to fetch movie data from TMDB.')
        else:
            messages.error(request, 'Form is not valid.')

        return render(request, self.template_name, {'form': form})

    def fetch_movie_data_from_tmdb(self, tmdb_id):
        """Fetch movie data from TMDB by movie ID."""
        api_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={settings.TMDB_API_KEY}&append_to_response=credits,videos"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        return None

    def create_movie_instance_from_tmdb_data(self, movie_data):
        """Create a Movie instance from TMDB data, extracting director, cast, and trailer link."""
        director = next((crew['name'] for crew in movie_data['credits']['crew'] if crew['job'] == 'Director'), None)
        cast = ', '.join([cast['name'] for cast in movie_data['credits']['cast'][:5]])  # Get top 5 cast members
        trailer_link = next((f"https://www.youtube.com/watch?v={video['key']}" for video in movie_data['videos']['results'] if video['type'] == 'Trailer'), None)

        if 'poster_path' not in movie_data:
            return None

        movie = Movie(
            tmdb_id=movie_data['id'],
            title=movie_data['title'],
            overview=movie_data['overview'],
            release_date=movie_data.get('release_date'),
            poster_path=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
            original_language=movie_data['original_language'],
            director=director,
            cast=cast,
            user_rating=movie_data.get('vote_average', 0),
            trailer_link=trailer_link,

        )
        return movie

class AdminMovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = 'movies/admin_movie_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser