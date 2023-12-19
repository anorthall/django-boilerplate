from django.test import TestCase

from .models import User


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            name="Test User",
            password="test",
        )

    def test_name(self):
        self.assertEqual(str(self.user), self.user.name)
        self.assertEqual(self.user.get_full_name(), self.user.name)
        self.assertEqual(self.user.get_short_name(), self.user.name)
