# import tempfile
# from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# from core import models


# Creating urls for making various api calls
USER_SIGNUP_URL = reverse("user:user-signup")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_student_user_success(self):
        """Test that student user creation with valid credential success"""
        payload = {
            'email': 'test@education.com',
            'password': 'Appis@404wrong',
            'username': 'testusername',
            'is_student': True,
            'is_teacher': False
        }

        res = self.client.post(USER_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=res.data['email'])
        self.assertEqual(user.username, payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)

    def test_create_valid_teacher_user_success(self):
        """Test that teacher user creation with valid credential success"""
        payload = {
            'email': 'test@education.com',
            'password': 'Appis@404wrong',
            'username': 'testusername',
            'is_student': False,
            'is_teacher': True
        }

        res = self.client.post(USER_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=res.data['email'])
        self.assertEqual(user.username, payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_student)

    def test_user_exists_fails(self):
        """Test that creating new user which already exists fails"""
        payload = {
            'email': 'abck22@gmail.com',
            'password': 'Test@123lifeisabitch',
            'username': 'testuser4',
            'is_teacher': True,
            'is_student': False
        }
        create_new_user(**payload)

        res = self.client.post(USER_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_creation_password_too_short(self):
        """Test that user creation with password too short fails"""
        payload = {
            'email': 'test1@gmail.com',
            'password': 'pas',
            'username': 'testusername',
            'is_teacher': True,
            'is_student': False
        }

        res = self.client.post(USER_SIGNUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(**payload).exists()
        self.assertFalse(user_exists)

    def test_get_not_allowed_on_user_signup_url(self):
        """Test that retrieving profile details of others fails"""
        create_new_user(**{
            'email': 'temp@curesio.com',
            'password': 'testpass@123df',
            'username': 'tempusername',
            'is_teacher': True,
            'is_student': False
        })

        res = self.client.get(USER_SIGNUP_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PrivateUserApiTests(TestCase):
    """Test API requests that requires authentication"""

    def setUp(self):
        self.user = create_new_user(**{
            'email': 'test@curesio.com',
            'password': 'testpass@1234',
            'username': 'testuser',
            'is_teacher': True,
            'is_student': False
        })

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_not_allowed_on_USER_SIGNUP_URL(self):
        """Test that retrieving profile details of others fails"""
        create_new_user(**{
            'email': 'temp@education.com',
            'password': 'testpass@123df',
            'username': 'testuser12',
            'is_teacher': True,
            'is_student': False
        })

        res = self.client.get(USER_SIGNUP_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
