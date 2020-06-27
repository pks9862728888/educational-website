from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core import models

# Urls for checking
institute_min_url = "institute:institute-min-details-teacher-admin"
INSTITUTE_MIN_DETAILS_TEACHER_URL = reverse(institute_min_url)
INSTITUTE_CREATE_BY_TEACHER_URL = reverse("institute:create")


def get_full_details_institute_url(slug_text):
    """Creates and returns institute full details url"""
    return reverse("institute:detail", kwargs={'institute_slug': slug_text})


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

    def test_get_not_allowed_on_institute_create_url(self):
        """Test that get request is not allowed for unauthenticated user"""
        res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_allowed_on_institute_create_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def get_not_allowed_on_institute_full_details_url(self):
        """Test that get is not allowed for unauthenticated user"""
        teacher_user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            password='temppassword',
            username='tempusername',
            is_teacher=True
        )
        institute = models.Institute.objects.create(
            user=teacher_user,
            name='temp name',
            institute_category=models.InstituteCategory.EDUCATION
        )
        res = self.client.post(get_full_details_institute_url(
            institute.institute_slug))

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

    def test_post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for authenticated teacher"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_institute_success_by_teacher(self):
        """Test that creating an institute with valid details is success"""
        payload = {
            'name': 'Name of institute',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'IN',
            'institute_profile': {
                'motto': '',
                'email': '',
                'phone': '',
                'website_url': '',
                'recognition': '',
                'state': '',
                'pin': '',
                'address': '',
                'primary_language': models.Languages.ENGLISH,
                'secondary_language': '',
                'tertiary_language': ''
            }
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL,
                               payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['created'], 'true')
        self.assertIn('url', res.data)
        self.assertTrue(models.Institute.objects.filter(
            name=payload['name'].lower()).exists())

        institute = models.Institute.objects.get(
            name=payload['name'].lower())
        institute_profile = models.InstituteProfile.objects.get(
            institute=institute)
        self.assertEqual(institute.name, payload['name'].lower())
        self.assertEqual(institute.country, payload['country'])
        self.assertEqual(institute.institute_category,
                         payload['institute_category'])
        self.assertEqual(institute_profile.motto,
                         payload['institute_profile']['motto'])
        self.assertEqual(institute_profile.email,
                         payload['institute_profile']['email'])
        self.assertEqual(institute_profile.phone,
                         payload['institute_profile']['phone'])
        self.assertEqual(institute_profile.website_url,
                         payload['institute_profile']['website_url'])
        self.assertEqual(institute_profile.recognition,
                         payload['institute_profile']['recognition'])
        self.assertEqual(institute_profile.state,
                         payload['institute_profile']['state'])
        self.assertEqual(institute_profile.pin,
                         payload['institute_profile']['pin'])
        self.assertEqual(institute_profile.address,
                         payload['institute_profile']['address'])
        self.assertEqual(institute_profile.primary_language,
                         payload['institute_profile']['primary_language'])
        self.assertEqual(institute_profile.secondary_language,
                         payload['institute_profile']['secondary_language'])
        self.assertEqual(institute_profile.tertiary_language,
                         payload['institute_profile']['tertiary_language'])

    def test_create_institute_full_details_success_by_teacher(self):
        """
        Test that creating an institute with
        full valid details is success
        """
        payload = {
            'name': 'Temp Institute',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US',
            'institute_profile': {
                'motto': 'Sample motto',
                'email': 'abc@gmail.com',
                'phone': '+919878787878',
                'website_url': 'http://www.google.com',
                'recognition': 'ICSE',
                'state': models.StatesAndUnionTerritories.ASSAM,
                'pin': '799878',
                'address': 'Dadra and nagar haveli, west district',
                'primary_language': models.Languages.HINDI,
                'secondary_language': models.Languages.ENGLISH,
                'tertiary_language': ''
            }
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL,
                               payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['created'], 'true')
        self.assertIn('url', res.data)
        self.assertTrue(models.Institute.objects.filter(
            name=payload['name'].lower()).exists())

        institute = models.Institute.objects.get(
            name=payload['name'].lower())
        institute_profile = models.InstituteProfile.objects.get(
            institute=institute)

        self.assertEqual(institute.name, payload['name'].lower())
        self.assertEqual(institute.country, payload['country'])
        self.assertEqual(institute.institute_category,
                         payload['institute_category'])
        self.assertEqual(institute_profile.motto,
                         payload['institute_profile']['motto'])
        self.assertEqual(institute_profile.email,
                         payload['institute_profile']['email'])
        self.assertEqual(institute_profile.phone,
                         payload['institute_profile']['phone'])
        self.assertEqual(institute_profile.website_url,
                         payload['institute_profile']['website_url'])
        self.assertEqual(institute_profile.recognition,
                         payload['institute_profile']['recognition'])
        self.assertEqual(institute_profile.state,
                         payload['institute_profile']['state'])
        self.assertEqual(institute_profile.pin,
                         payload['institute_profile']['pin'])
        self.assertEqual(institute_profile.address,
                         payload['institute_profile']['address'])
        self.assertEqual(institute_profile.primary_language,
                         payload['institute_profile']['primary_language'])
        self.assertEqual(institute_profile.secondary_language,
                         payload['institute_profile']['secondary_language'])
        self.assertEqual(institute_profile.tertiary_language,
                         payload['institute_profile']['tertiary_language'])

    def test_create_institute_name_required(self):
        """Test that creating institute with invalid details fails"""
        payload = {
            'name': '   ',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US'
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(models.Institute.objects.filter(
            user=self.user).exists())

    def test_institute_category_required(self):
        """Test that institute_category is required to create institute"""
        payload = {
            'name': '   ',
            'institute_category': '',
            'country': 'US'
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_institute_creation_fails_invalid_data(self):
        """Test that institute_category is required to create institute"""
        payload = {
            'name': 'test oomm',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US',
            'institute_profile': {
                'motto': 'Sample motto',
                'email': 'gmail.com',
                'phone': '78787878',
                'website_url': 'www.google.com'
            }
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(models.Institute.objects.filter(
            name=payload['name'].lower()).exists())

    def test_create_institute_in_other_teacher_name_fails(self):
        """Test that teacher can create institute in his name only"""
        new_user = create_teacher()
        payload = {
            'user': new_user,
            'name': '   ',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US'
        }
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(models.Institute.objects.filter(
            user=new_user).exists())
        self.assertFalse(models.Institute.objects.filter(
            user=self.user).exists())

    def test_duplicate_institute_fails(self):
        """Test that teacher can not create a duplicate institute"""
        payload = {
            'name': '   ',
            'institute_category': models.InstituteCategory.EDUCATION,
            'country': 'US'
        }
        self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_success_on_institute_full_details_url(self):
        """Test that teacher can get full details of institute"""
        institute = models.Institute.objects.create(
            user=self.user,
            name='temp institute',
            institute_category=models.InstituteCategory.EDUCATION
        )

        res = self.client.get(get_full_details_institute_url(
            institute.institute_slug))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'temp institute')
        self.assertIn('institute_profile', res.data)
        self.assertIn('institute_logo', res.data)
        self.assertIn('institute_banner', res.data)


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

    def test_post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "user": self.user,
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_allowed_on_institute_create_url(self):
        """Test that get request is not allowed for student user"""
        res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_not_allowed_on_institute_create_url(self):
        """Test that post is not allowed for student user"""
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def get_not_allowed_on_institute_full_details_url(self):
        """Test that get is not allowed for student user"""
        teacher_user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            password='temppassword',
            username='tempusername',
            is_teacher=True
        )
        institute = models.Institute.objects.create(
            user=teacher_user,
            name='temp name',
            institute_category=models.InstituteCategory.EDUCATION
        )
        res = self.client.post(
            get_full_details_institute_url(institute.institute_slug))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedUserAPITests(TestCase):
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

    def test_post_not_allowed_on_institute_min_details_teacher_url(self):
        """Test that post is not allowed for unauthenticated user"""
        res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_allowed_on_institute_create_url(self):
        """Test that get request is not allowed for staff user"""
        res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_not_allowed_on_institute_create_url(self):
        """Test that post is not allowed for staff user"""
        res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
            "name": "Temp name",
            "institute_category": models.InstituteCategory.EDUCATION
        })

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def get_not_allowed_on_institute_full_details_url(self):
        """Test that get is not allowed for normal authenticated user"""
        teacher_user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            password='temppassword',
            username='tempusername',
            is_teacher=True
        )
        institute = models.Institute.objects.create(
            user=teacher_user,
            name='temp name',
            institute_category=models.InstituteCategory.EDUCATION
        )
        res = self.client.post(
            get_full_details_institute_url(institute.institute_slug))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
