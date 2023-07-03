from django.test import Client, TestCase
from django.urls import reverse

from .models import AppUser


class AuthenticationUnitTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = AppUser.objects.create_user(
            email="test@user.app",
            name="Test User",
            password="password",
        )
        self.user.is_active = True
        self.user.save()

    def test_str(self):
        """Test that the string representation of a user is correct"""
        self.assertEqual(str(self.user), "Test User")

    def test_get_short_name(self):
        """Test that the short name of a user is correct"""
        self.assertEqual(self.user.get_short_name(), "Test")

    def test_get_full_name(self):
        """Test that the full name of a user is correct"""
        self.assertEqual(self.user.get_full_name(), "Test User")

    def test_create_user_with_invalid_data(self):
        """Test creating a user with invalid data"""
        with self.assertRaises(ValueError):
            AppUser.objects.create_user(email="", name="")

        with self.assertRaises(ValueError):
            AppUser.objects.create_user(email="noname@user.app", name="")

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = AppUser.objects.create_superuser(
            email="superuser@user.app",
            name="Super User",
            password="password",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)


class AuthenticationIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = AppUser.objects.create_user(
            email="test@user.app",
            name="Test User",
            password="password",
        )
        self.user.is_active = True
        self.user.save()

    def test_login(self):
        """Test that a user can log in using the login form"""
        response = self.client.get(reverse("core:login"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("core:login"),
            {
                "username": self.user.email,
                "password": "password",
            },
            follow=True,
        )
        self.assertContains(response, "You are now logged in.")

    def test_login_with_incorrect_password(self):
        """Test that a user cannot log in with an incorrect password"""
        response = self.client.post(
            reverse("core:login"),
            {
                "username": self.user.email,
                "password": "incorrect password",
            },
            follow=True,
        )
        self.assertContains(
            response, "Please enter a correct email address and password."
        )

    def test_logout(self):
        """Test that a user can log out"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have been logged out.")

    def test_register(self):
        """Test that a user can register"""
        response = self.client.get(reverse("core:register"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("core:register"),
            {
                "email": "register@user.app",
                "name": "Register User",
                "password1": "password",
                "password2": "password",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Your account has been created. You can now log in.",
        )

        user = AppUser.objects.get(email="register@user.app")
        self.assertEqual(user.name, "Register User")

    def test_register_with_mismatched_passwords(self):
        """Test that a user cannot register with mismatched passwords"""
        response = self.client.post(
            reverse("core:register"),
            {
                "email": "register@user.app",
                "name": "Register User",
                "password1": "password",
                "password2": "incorrect password",
            },
            follow=True,
        )
        self.assertContains(response, "Passwords do not match")

    def test_password_change(self):
        """Test that a user can change their password"""
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:password_change"), follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("core:password_change"),
            {
                "old_password": "password",
                "new_password1": "new password",
                "new_password2": "new password",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your password has been changed.")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new password"))
