import os
import datetime

from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from core import models


class UserModelTests(TestCase):

    def test_create_user_model_with_email_successful(self):
        """Test whether creating new user with email is successful"""
        email = "test1@server.com"
        password = "testpassword@123"
        username = "testuser"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email for new user is normalized"""
        email = "test@servEr.CoM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test_pass@123',
            username='testuser'
        )

        self.assertEqual(user.email, email.lower())

    def test_email_required(self):
        """Test that email is required to create a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '', 'testPass', 'testuser')
            get_user_model().objects.create_user(
                ' ', 'testPass', 'testuser')

    def test_username_required(self):
        """Test that username is required to create a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test@gmail.com', 'testPass', ''
            )
            get_user_model().objects.create_user(
                'test@gmail.com', 'testPass', ' '
            )

    def test_create_superuser_successful(self):
        """Test that creating superuser is successful"""
        email = 'test@gmail.com'
        password = 'trst@1234a'
        username = 'testuser'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_student)
        self.assertFalse(user.is_teacher)

    def test_create_student_successful(self):
        """Test that creating student is successful"""
        email = 'test@gmail.com'
        password = 'trst@1234a'
        username = 'testuser'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            username=username,
            is_student=True
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)

    def test_create_teacher_successful(self):
        """Test that creating superuser is successful"""
        email = 'test@gmail.com'
        password = 'trst@1234a'
        username = 'testuser'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            username=username,
            is_teacher=True
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_student)
        self.assertTrue(user.is_teacher)

    def test_user_string_representation(self):
        """Test the string representation of user model"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test@pass2',
            username='sampleuser'
        )

        self.assertEqual(str(user), email)


class TeacherModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            password='testpassword',
            username='testusername',
            is_teacher=True
        )

    def test_profile_created_when_user_created(self):
        """Test teacher profile is created when user registers"""
        user = get_object_or_404(models.UserProfile, user=self.user)

        self.assertEqual(str(self.user), str(user))

    def test_create_user_profile_created_successfully(self):
        """Test that profile is created successfully with full details"""
        payload = {
            'first_name': 'Temp name',
            'last_name': 'Lastname',
            'phone': '+919862727348',
            'gender': 'M',
            'birthday': '1997-12-23',             # YYYY-MM-DD
            'country': 'IN',
            'language': models.Languages.HINDI
        }

        self.user.user_profile.first_name = payload['first_name']
        self.user.user_profile.last_name = payload['last_name']
        self.user.user_profile.phone = payload['phone']
        self.user.user_profile.gender = payload['gender']
        self.user.user_profile.country = payload['country']
        self.user.user_profile.secondary_language = payload['language']
        self.user.save()
        self.user.refresh_from_db()

        self.assertEqual(self.user.user_profile.first_name,
                         payload['first_name'].upper())
        self.assertEqual(self.user.user_profile.last_name,
                         payload['last_name'].upper())
        self.assertEqual(self.user.user_profile.phone, payload['phone'])
        self.assertEqual(self.user.user_profile.gender, payload['gender'])
        self.assertEqual(self.user.user_profile.country, payload['country'])
        self.assertEqual(self.user.user_profile.primary_language,
                         models.Languages.ENGLISH)
        self.assertEqual(
            self.user.user_profile.secondary_language, payload['language'])
        self.assertEqual(self.user.user_profile.tertiary_language, None)

    def test_string_representation_of_user_profile(self):
        """Test the string representation of teacher profile model"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass@1234',
            username='testuser',
            is_teacher=True
        )
        user_profile = models.UserProfile.objects.get(user=user)

        self.assertEqual(str(user_profile), email)

    @patch('uuid.uuid4')
    def test_image_upload_url_uuid(self, mock_url):
        """Test that teacher profile picture is uploaded in correct location"""
        uuid = 'test-uuid'
        mock_url.return_value = uuid
        file_path = models.user_profile_picture_upload_file_path(
            None, 'img.jpg')
        dt = datetime.date.today()
        path = 'pictures/uploads/user/profile'
        ini_path = f'{path}/{dt.year}/{dt.month}/{dt.day}'
        expected_path = os.path.join(ini_path, f'{uuid}.jpg')
        self.assertEqual(file_path, expected_path)
