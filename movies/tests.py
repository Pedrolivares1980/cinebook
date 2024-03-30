from django.test import TestCase
from .models import Movie
from .forms import MovieForm
from django.urls import reverse, resolve
from .views import MovieListView, MovieDetailView
from django.contrib.auth.models import User
from datetime import date

class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie = Movie.objects.create(
            title="Test Movie",
            tmdb_id=12345, 
            director="Test Director",
            cast="Test Cast",
            user_rating=7.5,
            trailer_link="http://example.com/trailer",
            overview="Test Overview",
            release_date=date.today(),
            poster_path="http://example.com/poster.jpg",
            original_language="en"
        )

    def test_movie_creation(self):
        self.assertTrue(isinstance(self.movie, Movie))
        self.assertEqual(str(self.movie), self.movie.title)

    def test_movie_deletion(self):
        movie_id = self.movie.id
        self.movie.delete()
        self.assertFalse(Movie.objects.filter(id=movie_id).exists())
class MovieFormTest(TestCase):

    def test_movie_form_valid(self):
        form_data = {
            'title': "Test Movie",
            'tmdb_id': 123,
            'director': "Test Director",
            'cast': "Test Cast",
            'user_rating': 5.0,
            'trailer_link': "http://example.com/trailer",
            'overview': "Test overview",
            'release_date': date.today(),
            'poster_path': "http://example.com/poster.jpg",
            'original_language': "en"
        }
        form = MovieForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_movie_form_invalid(self):
        form_data = {} 
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())

class AdminMovieCreateViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', email='staff@example.com', password='test')
        self.staff_user.is_staff = True
        self.staff_user.save()

    def test_view_url_accessible_by_name(self):
        self.client.login(username='staff', password='test')
        response = self.client.get(reverse('admin_movie_create'))
        self.assertEqual(response.status_code, 200)


class AdminMovieDeleteViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', email='staff@example.com', password='test', is_staff=True)
        self.non_staff_user = User.objects.create_user(username='nonstaff', password='12345')
        self.movie = Movie.objects.create(
            title="Test Movie", 
            tmdb_id=12345,  
            director="Test Director",
            cast="Test Cast",
            user_rating=7.5,
            trailer_link="http://example.com/trailer",
            overview="Test Overview",
            release_date=date.today(),
            poster_path="http://example.com/poster.jpg",
            original_language="en"
        )

    def test_movie_deletion_by_staff_user(self):
        self.client.login(username='staff', password='test')
        response = self.client.post(reverse('admin_movie_delete', args=[self.movie.pk]))
        self.assertRedirects(response, reverse('admin_dashboard')) 
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

class MovieUrlsTest(TestCase):

    def test_movie_list_url_resolves(self):
        url = reverse('movie_list')
        self.assertEqual(resolve(url).func.view_class, MovieListView)

    def test_movie_detail_url_resolves(self):
        url = reverse('movie_detail', args=['1'])
        self.assertEqual(resolve(url).func.view_class, MovieDetailView)