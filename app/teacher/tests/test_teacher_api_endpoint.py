from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models

# Urls for running the tests
CREATE_CLASSROOM_URL = reverse("teacher:create-classroom")
CREATE_SUBJECT_URL = reverse("teacher:create-subject")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicAPItests(TestCase):
    """Tests for public api"""

    def setUp(self):
        self.client = APIClient()

    def test_get_request_not_allowed_create_classroom_url(self):
        """Test that get request is not allowed on user classroom url"""
        res = self.client.get(CREATE_CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classroom_post_not_allowed_unauthenticated_user(self):
        """Test that unauthenticated user can not make post request"""
        user = create_new_user(**{
            'email': 'testuser@gmail.com',
            'username': 'testusername',
            'password': 'testpass@1234'
        })
        res = self.client.post(
            CREATE_CLASSROOM_URL, {'user': [user.pk], 'name': 'testclass'})

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

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

        self.classroom = models.Classroom.objects.create(
            user=self.user_teacher,
            name='Classroomname'
        )

    def test_create_classroom_successful(self):
        """Test that creating classroom is successful for teacher"""
        payload = {
            'name': 'Tempsubject'
        }

        res = self.client.post(CREATE_CLASSROOM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'].lower())

    def test_classroom_name_required(self):
        """Test that classroom name required"""
        payload = {
            'name': ' '
        }

        res = self.client.post(CREATE_CLASSROOM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_classroom_name_less_than_4_characters_fails(self):
        """Test that min length of classroom name is 4 chars"""
        payload = {
            'name': 'aa'
        }

        res = self.client.post(CREATE_CLASSROOM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_classroom_creation_fails(self):
        """Test that creating duplicate classroom fails"""
        self.client.post(CREATE_CLASSROOM_URL, {'name': 'classn'})
        res = self.client.post(CREATE_CLASSROOM_URL, {'name': 'classn'})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_not_allowed_on_create_classroom_url(self):
        """Test that get is not allowed on create classroom url"""
        res = self.client.get(CREATE_CLASSROOM_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_subject_successful(self):
        """Test that creating subject is successful for teacher"""
        payload = {
            'classroom': self.classroom.pk,
            'name': 'Tempsubject'
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'].lower())
        self.assertEqual(res.data['classroom'], payload['classroom'])

    def test_subject_name_required(self):
        """Test that subject name required"""
        payload = {
            'classroom': self.classroom.pk,
            'name': ' '
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subject_name_less_than_4_characters_fails(self):
        """Test that min length of subject name is 4 chars"""
        payload = {
            'classroom': self.classroom.pk,
            'name': 'aa'
        }

        res = self.client.post(CREATE_SUBJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_subject_creation_fails(self):
        """Test that creating duplicate subject fails"""
        self.client.post(CREATE_SUBJECT_URL, {
                         'classroom': self.classroom.pk,
                         'name': 'subname'})
        res = self.client.post(CREATE_SUBJECT_URL, {
                               'classroom': self.classroom.pk,
                               'name': 'subname'})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_not_allowed_on_create_subject_url(self):
        """Test that get is not allowed on create subject url"""
        res = self.client.get(CREATE_SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_creating_subject_with_another_persons_classroom_fails(self):
        """Test that you cannot create subject with other persons classroom"""
        user = create_new_user(**{
            'email': 'testusdser@gmail.com',
            'username': 'tesstdusername',
            'password': 'testpaass@1234',
            'is_teacher': True
        })
        classroom = models.Classroom.objects.create(
            user=user,
            name='tempclass'
        )

        res = self.client.post(CREATE_SUBJECT_URL, {
            'classroom': classroom.pk,
            'name': 'subjectname'
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
