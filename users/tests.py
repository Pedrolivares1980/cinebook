from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm
import os
from shutil import rmtree


# Import settings to access BASE_DIR
from django.conf import settings

class UserFormsTests(TestCase):
    """
    Tests user-related forms including registration, profile update, and user update.
    """

    def setUp(self):
        # Setup for form tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.get_or_create(user=self.user)

    def test_user_register_form(self):
        # Test the user registration form with valid data
        form_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'django1234', 'password2': 'django1234'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())



class UserViewsTests(TestCase):
    """
    Tests user-related views including login, logout, profile view, and registration.
    """

    def setUp(self):
        # Setup for view tests
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')


    def test_login_with_invalid_data(self):
        # Test login with invalid data
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password': 'password'})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == "Username or Password is incorrect." for msg in messages))


    def test_profile_update_with_valid_data(self):
        # Test updating profile with valid data
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {'username': 'updatedusername', 'email': 'updatedemail@example.com'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updatedemail@example.com')


class ProfileModelTest(TestCase):
    """
    Tests for the Profile model
    """

    @classmethod
    def setUpTestData(cls):
        # Ensure the test_media directory exists
        cls.test_media_path = os.path.join(settings.BASE_DIR, 'test_media')
        os.makedirs(cls.test_media_path, exist_ok=True)

        # Copy the default.jpg image to the test_media directory
        default_image_path = os.path.join(settings.BASE_DIR, 'media', 'default.jpg')
        test_image_path = os.path.join(cls.test_media_path, 'default.jpg')
        if not os.path.exists(test_image_path):
            with open(default_image_path, 'rb') as f_src, open(test_image_path, 'wb') as f_dst:
                f_dst.write(f_src.read())

    @classmethod
    def tearDownClass(cls):
        # Clean up the test_media directory after all tests have run
        rmtree(cls.test_media_path)
        super().tearDownClass()


