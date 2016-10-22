from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import InvestUser


class InvestUserTestCase(TestCase):
    def setUp(self):
        testuser = InvestUser.objects.create(username='testuser')

    def test_user_can_create(self):
        """
        Create user test
        """
        testuser = get_object_or_404(InvestUser, username='testuser')
        self.assertEqual(testuser.username, 'testuser')
