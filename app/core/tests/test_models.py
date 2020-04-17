from django.test import TestCase
from django.contrib.auth import get_user_model


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

    def test_user_string_representation(self):
        """Test the string representation of user model"""
        email = 'test@gmail.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test@pass2',
            username='sampleuser'
        )

        self.assertEqual(str(user), email)
