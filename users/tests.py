from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image
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

    def test_user_update_form(self):
        # Test the user update form with valid data
        form_data = {'username': 'updateduser', 'email': 'updateuser@example.com'}
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_update_form(self):
        # Test the profile update form with invalid image format
        with open('invalid_image.txt', 'wb') as f:
            f.write(b'this is not an image file')
        with open('invalid_image.txt', 'rb') as f:
            form_data = {'image': f}
            form = ProfileUpdateForm(data={}, files=form_data, instance=self.user.profile)
            self.assertFalse(form.is_valid())
        os.remove('invalid_image.txt')


class UserViewsTests(TestCase):
    """
    Tests user-related views including login, logout, profile view, and registration.
    """

    def setUp(self):
        # Setup for view tests
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')

    def test_login_view(self):
        # Test successful login
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('blog-home'))

    def test_login_with_invalid_data(self):
        # Test login with invalid data
        response = self.client.post(reverse('login'), {'username': 'wrong', 'password': 'password'})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(msg.message == "Username or Password is incorrect." for msg in messages))

    def test_logout_view(self):
        # Test logout functionality
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('blog-home'))

    def test_profile_access_without_login(self):
        # Test profile access without login redirects to login page
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

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

    def create_test_image(self):
        # Create an in-memory test image
        img = Image.new('RGB', (1000, 1000), color='red')
        img_file = BytesIO()
        img.save(img_file, format='JPEG')
        img_file.name = 'test.jpg'
        img_file.seek(0)
        return img_file

    def test_image_resizing(self):
        # Test that a user's profile image is resized correctly
        with override_settings(MEDIA_ROOT=self.test_media_path):
            img_file = self.create_test_image()
            user = User.objects.create_user(username='user2', password='pass')
            profile = Profile.objects.get(user=user)
            profile.image.save('test_image.jpg', ImageFile(img_file))
            
            resized_img = Image.open(profile.image.path)
            self.assertTrue(resized_img.width <= 200 and resized_img.height <= 200)


