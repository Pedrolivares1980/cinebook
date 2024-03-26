from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cinema

User = get_user_model()

class CinemaModelTests(TestCase):
    """Tests to ensure the Cinema model is working correctly."""

    def test_cinema_creation(self):
        """Test creating a Cinema and verify its string representation."""
        cinema = Cinema.objects.create(
            name="Test Cinema",
            address="123 Test St",
            phone_number="1234567890"
        )
        self.assertEqual(cinema.name, "Test Cinema")
        self.assertEqual(str(cinema), "Test Cinema")


class CinemaViewTests(TestCase):
    """Tests to verify views handle permissions and actions correctly."""

    @classmethod
    def setUpTestData(cls):
        """Create initial data for tests."""
        cls.user_staff = User.objects.create_user(
            username="staff", email="staff@test.com", password="testpass123", is_staff=True)
        cls.user_nonstaff = User.objects.create_user(
            username="user", email="user@test.com", password="testpass123")

        cls.cinema = Cinema.objects.create(
            name="Cinema for Tests",
            address="123 Test Lane",
            phone_number="9876543210"
        )

    def test_cinema_create_view_permission(self):
        """Ensure only staff users can access the cinema create page."""
        self.client.login(username="user", password="testpass123")
        response = self.client.get(reverse('cinema_add'))
        # Expecting redirect to login page for non-staff user
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username="staff", password="testpass123")
        response = self.client.get(reverse('cinema_add'))
        self.assertEqual(response.status_code, 200)


    def test_cinema_update_view_permission(self):
        """Test permissions for accessing the cinema update view."""
        update_url = reverse('cinema_edit', args=[self.cinema.pk])
        response = self.client.get(update_url)
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='user', password='testpass123')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='staff', password='testpass123')
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

    def test_cinema_delete_view_no_login(self):
        """Test that unauthenticated users are redirected to the login page."""
        response = self.client.get(reverse('cinema_delete', kwargs={'pk': self.cinema.pk}), follow=True)
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('cinema_delete', kwargs={'pk': self.cinema.pk})}")

    def test_cinema_delete_view_non_staff(self):
        """Ensure non-staff users cannot access the cinema delete view."""
        self.client.login(username='user', password='testpass123')
        response = self.client.get(reverse('cinema_delete', kwargs={'pk': self.cinema.pk}))
        self.assertEqual(response.status_code, 403)

    def test_cinema_delete_view_staff(self):
        """Staff users can access the cinema delete view."""
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(reverse('cinema_delete', kwargs={'pk': self.cinema.pk}))
        self.assertEqual(response.status_code, 200)

    def test_cinema_delete_functionality(self):
        """Test the actual delete functionality for staff users."""
        self.client.login(username='staff', password='testpass123')
        response = self.client.post(reverse('cinema_delete', kwargs={'pk': self.cinema.pk}), follow=True)
        self.assertRedirects(response, reverse('admin_dashboard'))
        with self.assertRaises(Cinema.DoesNotExist):
            Cinema.objects.get(pk=self.cinema.pk)
