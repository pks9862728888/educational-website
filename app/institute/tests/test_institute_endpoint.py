from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core import models

# Urls for checking
institute_min_url = "institute:institute-min-details-teacher-admin"
INSTITUTE_MIN_DETAILS_TEACHER_URL = reverse(institute_min_url)


def create_teacher(email='abc@gmail.com', username='tempusername'):
    """Creates and return teacher"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_teacher=True
    )


def create_student(email='abc@gmail.com', username='tempusername'):
    """Creates and return student"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_student=True
    )


class PublicInstituteApiTests(TestCase):
    """Tests the institute api for unauthenticated user"""

    def setUp(self):
        """Setup code for all test cases"""
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testusername',
            password='testpassword',
            is_teacher=True
        )
        self.client = APIClient()

    def test_get_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that get request is not allowed for unauthenticated user"""
        res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTeacherUserAPITests(TestCase):
    """Tests for authenticated teacher user"""

    def setUp(self):
        """Setup code for all test cases"""
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testusername',
            password='testpassword',
            is_teacher=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_success_institute_min_endpoint_teacher(self):
        """Test that get request is success for teacher"""
        payload = {
            'name': 'Temp Institute',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US',
            'institute_profile': {
                'motto': 'Sample motto',
                'email': 'abc@gmail.com',
                'phone': '+919878787878',
                'website_url': 'www.google.com',
                'recognition': 'ICSE',
                'state': models.StatesAndUnionTerritories.ASSAM
            }
        }
        institute = models.Institute.objects.create(
            user=self.user,
            name=payload['name'],
            country=payload['country'],
            institute_category=payload['institute_category']
        )
        institute_profile = payload['institute_profile']
        institute.institute_profile.motto = institute_profile['motto']
        institute.institute_profile.email = institute_profile['email']
        institute.institute_profile.phone = institute_profile['phone']
        institute.institute_profile.website_url = institute_profile[
            'website_url']
        institute.institute_profile.recognition = institute_profile[
            'recognition']
        institute.institute_profile.state = institute_profile['state']
        institute.save()

        res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data[0]['user'], self.user.pk)
        self.assertEqual(res.data[0]['name'], payload['name'].lower())
        self.assertEqual(res.data[0]['institute_category'],
                         payload['institute_category'])
        self.assertEqual(res.data[0]['country'], payload['country'])
        self.assertEqual(res.data[0]['institute_profile']['motto'],
                         payload['institute_profile']['motto'])
        self.assertEqual(res.data[0]['institute_profile']['email'],
                         payload['institute_profile']['email'])
        self.assertEqual(res.data[0]['institute_profile']['phone'],
                         payload['institute_profile']['phone'])
        self.assertEqual(res.data[0]['institute_profile']['website_url'],
                         payload['institute_profile']['website_url'])
        self.assertEqual(res.data[0]['institute_profile']['recognition'],
                         payload['institute_profile']['recognition'])
        self.assertEqual(res.data[0]['institute_profile']['state'],
                         payload['institute_profile']['state'])
        self.assertEqual(list(res.data[0]['institute_logo']), [])

    def test_get_other_institute_fail_institute_min_endpoint_teacher(self):
        """Test that un-enrolled institute can not be get by teacher"""
        models.Institute.objects.create(
            user=self.user,
            name='Temp Institute',
            institute_category=models.InstituteCategory.EDUCATION
        )
        models.Institute.objects.create(
            user=create_teacher(),
            name='Temp Institute',
            institute_category=models.InstituteCategory.EDUCATION
        )
        res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for authenticated teacher"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedStudentUserAPITests(TestCase):
    """Tests for authenticated student user"""

    def setUp(self):
        """Setup code for all test cases"""
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testusername',
            password='testpassword',
            is_student=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that get request is not allowed for unauthenticated user"""
        res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedStaffUserAPITests(TestCase):
    """Tests for authenticated user"""

    def setUp(self):
        """Setup code for all test cases"""
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testusername',
            password='testpassword',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that get request is not allowed for unauthenticated user"""
        res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
