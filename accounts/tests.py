from django.test import TestCase

from .models import InvestUser


class InvestUserTestCase(TestCase):
    def setUp(self):
        testuser = InvestUser.objects.create(username='testuser')

    def test_user_can_create(self):
        """
        Create user test
        """
        testuser = InvestUser.objects.get_or_404(username='testuser')
        self.assertEqual(testuser.username, 'testuser')
