from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# from core import models

# Urls for running the tests
CREATE_SUBJECT_URL = reverse("teacher:create-subject")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicAPItests(TestCase):
    """Tests for public api"""

    def setUp(self):
        self.client = APIClient()

    def test_get_request_not_allowed_create_subject_url(self):
        """Test that get request is not allowed on user subject url"""
        res = self.client.get(CREATE_SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_allowed_unauthenticated_user(self):
        """Test that unauthenticated user can not make post requrest"""
        user = create_new_user(**{
            'email': 'testuser@gmail.com',
            'username': 'testusername',
            'password': 'testpass@1234'
        })
        res = self.client.post(
            CREATE_SUBJECT_URL, {'user': [user.pk], 'name': 'testsubject'})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_delete_not_allowed_unauthenticated_user:
    #     """Test deleting a subject not allowed unauthenticated user"""
    #     user = create_new_user(**{
    #         'email': 'testuser@gmail.com',
    #         'username': 'testusername'
    #         'password': 'testpass@1234'
    #         'is_teacher': True
    #     })

    #     subject = models.Subject.objects.create(
    #         user=user,
    #         name='subjectname'
    #     )

    #     res = self.client.delete(
    #         CREATE_REMOVE_SUBJECT_URL, {
    #             subject.
    #         }
    #     )


class privateTeacherAPITests(TestCase):
    """Tests for authenticated user who is a teacher"""

    def setUp(self):
        self.user_teacher = create_new_user(**{
            'email': 'test@curesio.com',
            'password': 'testpass@1234',
            'username': 'testuser',
            'is_teacher': True
        })

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_teacher)

    def test_create_subject_successful(self):
        """Test that creating subject is successful for teacher"""
        payload = {
            'user': [self.user_teacher.pk],
            'name': 'Tempsubject'
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'].lower())

    def test_subject_name_required(self):
        """Test that subject name required"""
        payload = {
            'user': [self.user_teacher.pk],
            'name': ' '
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subject_name_less_than_4_characters_fails(self):
        """Test that min length of subject name is 4 chars"""
        payload = {
            'user': [self.user_teacher.pk],
            'name': 'aa'
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_not_allowed_on_create_subject_url(self):
        """Test that get is not allowed on create subject url"""
        res = self.client.get(CREATE_SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
