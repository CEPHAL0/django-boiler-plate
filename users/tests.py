# users/tests/test_views.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserViewsTestCase(APITestCase):
    """
    Test suite for user-related views using session authentication.
    Covers: CSRF, registration, login, logout, who_am_i, fetch users, and admin check.
    """

    def setUp(self):
        # URLs
        self.csrf_url = reverse('get_csrf_token')
        self.register_url = reverse('register_user')
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        self.whoami_url = reverse('who_am_i')
        self.users_url = reverse('fetch_all_users')
        self.check_admin_url = reverse('check_admin')

        # Create test users
        self.regular_user = User.objects.create_user(
            username='regular_user',
            password='#RegularUser123',
            email='regularuser@gmail.com'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='#Admin1234',
            email='admin@gmail.com'
        )

    def test_get_csrf_token(self):
        """Test that CSRF token is set in cookies."""
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'CSRF cookie set')
        self.assertIn('csrftoken', response.cookies, "CSRF token cookie not set")


    def test_register_user_success(self):
        """Test successful user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'mismatched'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertFalse(User.objects.filter(username='newuser').exists())
    #
    def test_register_user_duplicate_username(self):
        """Test registration fails with duplicate username."""
        data = {
            'username': 'regular_user',  # already exists
            'email': 'other@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(self.register_url, data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)