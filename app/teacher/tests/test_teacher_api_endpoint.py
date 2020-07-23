from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models

# Urls for running the tests
CREATE_RETRIEVE_UPDATE_user_profile_URL = reverse("teacher:teacher-profile")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicAPItests(TestCase):
    """Tests for public api"""

    def setUp(self):
        self.client = APIClient()

    def test_get_user_profile_not_allowed_for_unauthorized_user(self):
        """Test that unauthorized user can not retrieve details"""
        res = self.client.get(CREATE_RETRIEVE_UPDATE_user_profile_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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

    def test_get_successful_authorized_teacher(self):
        """Test that authenticated teacher can see their profile details"""
        res = self.client.get(CREATE_RETRIEVE_UPDATE_user_profile_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.user_teacher))
        self.assertEqual(res.data['user_profile']['first_name'], '')
        self.assertEqual(res.data['user_profile']['last_name'], '')
        self.assertEqual(res.data['user_profile']['phone'], None)
        self.assertEqual(res.data['user_profile']['gender'], '')
        self.assertEqual(res.data['user_profile']['country'], 'IN')
        self.assertEqual(res.data['user_profile']['date_of_birth'], None)
        self.assertIn('created_date', res.data)
        self.assertEqual(res.data['username'], 'testuser')
        self.assertEqual(res.data['user_profile']['primary_language'],
                         models.Languages.ENGLISH)
        self.assertEqual(res.data['user_profile']
                         ['secondary_language'], None)
        self.assertEqual(res.data['user_profile']
                         ['tertiary_language'], None)

    def test_update_successful_authorized_teacher(self):
        """Test that authenticated teacher can see their profile details"""
        payload = {
            'username': 'changedusername',
            'user_profile': {
                'first_name': 'teacheR',
                'last_name': 'lastName',
                'phone': '+919876543234',
                'gender': 'M',
                'country': 'IN',
                'date_of_birth': '1997-12-23',
                'primary_language': 'BN',
                'secondary_language': 'HI',
                'tertiary_language': '',
            }
        }

        res = self.client.patch(CREATE_RETRIEVE_UPDATE_user_profile_URL,
                                payload, format='json')
        res_profile = dict(res.data['user_profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.user_teacher))
        self.assertEqual(res.data['username'], payload['username'])
        self.assertEqual(res_profile['first_name'],
                         payload['user_profile']['first_name'].upper())
        self.assertEqual(res_profile['last_name'],
                         payload['user_profile']['last_name'].upper())
        self.assertEqual(res_profile['phone'],
                         payload['user_profile']['phone'])
        self.assertEqual(res_profile['gender'],
                         payload['user_profile']['gender'])
        self.assertEqual(res_profile['country'],
                         payload['user_profile']['country'])
        self.assertEqual(res_profile['date_of_birth'],
                         payload['user_profile']['date_of_birth'])
        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['primary_language'],
                         payload['user_profile']['primary_language'])
        self.assertEqual(res_profile['secondary_language'],
                         payload['user_profile']['secondary_language'])
        self.assertEqual(res_profile['tertiary_language'], '')

    def test_post_create_retrieve_update_not_allowed(self):
        """Test that post is not allowed on create retrieve update url"""
        res = self.client.post(CREATE_RETRIEVE_UPDATE_user_profile_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# class TeacherImageUploadTests(TestCase):
#     """Tests for uploading teacher profile picture"""

#     def setUp(self):
#         """Setup for running all the tests"""
#         self.teacher_user = get_user_model().objects.create_user(
#             email='temp@curesio.com',
#             password='testpass@4',
#             username='tempuser4',
#             is_teacher=True
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(self.user)

#     def tearDown(self):
#         """Clean up code after running the tests"""
#         self.teacher_user.user_profile.image.delete()

#     def test_user_profile_picture_upload(self):
#         """Test that uploading teacher profile picture is successful"""
#         image_upload_url = create_user_image_upload_url()

#         with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
#             img = Image.new('RGB', (10, 10))
#             img.save(ntf, format='JPEG')
#             ntf.seek(0)
#             res = self.client.post(
#                 image_upload_url,
#                 {'image': ntf},
#                 format="multipart"
#             )

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn('image', res.data)

#     def test_user_profile_picture_invalid_image_fails(self):
#         """Test that invalid image upload fails"""
#         image_upload_url = create_user_image_upload_url()

#         res = self.client.post(
#             image_upload_url,
#             {'image': 'invalid image'},
#             format="multipart"
#         )

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
