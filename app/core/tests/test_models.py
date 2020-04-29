from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

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


class SubjectModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='abcd@gmail.com',
            password='testuser@1234',
            username='testusername',
            is_teacher=True
        )

    def test_create_subject_with_valid_details_success(self):
        """Test that creating subject with valid details success"""
        subject = models.Subject.objects.create(user=self.user,
                                                name='Science')

        self.assertTrue(models.Subject.objects.filter(
            name='science').exists()
        )
        self.assertEqual(subject.user, self.user)
        self.assertEqual(subject.name, 'science')

    def test_create_subject_name_required(self):
        """Test that creating subject with no name fails"""
        with self.assertRaises(ValueError):
            models.Subject.objects.create(user=self.user, name=' ')

    def test_create_model_fails_non_teacher_user(self):
        user1 = get_user_model().objects.create_user(
            email='emailse@gmail.com',
            username="tempusername",
            password='tempwasswordr3',
            is_student=True
        )

        with self.assertRaises(PermissionDenied):
            models.Subject.objects.create(user=user1, name='tempss')

    def test_string_representation_subject_model(self):
        """Test stirng representation of subject model"""
        subject = models.Subject.objects.create(user=self.user,
                                                name='Biology')

        self.assertEqual(str(subject), 'biology')
