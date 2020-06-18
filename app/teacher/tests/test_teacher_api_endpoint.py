from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models

# Urls for running the tests
CREATE_CLASSROOM_URL = reverse("teacher:create-classroom")
CREATE_SUBJECT_URL = reverse("teacher:create-subject")
CREATE_RETRIEVE_UPDATE_TEACHER_PROFILE_URL = reverse("teacher:teacher-profile")


def create_new_user(**kwargs):
    """Creates a new user"""
    return get_user_model().objects.create_user(**kwargs)


class PublicAPItests(TestCase):
    """Tests for public api"""

    def setUp(self):
        self.client = APIClient()

    def test_get_teacher_profile_not_allowed_for_unauthorized_user(self):
        """Test that unauthorized user can not retrieve details"""
        res = self.client.get(CREATE_RETRIEVE_UPDATE_TEACHER_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

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

    def test_get_successful_authorized_teacher(self):
        """Test that authenticated teacher can see their profile details"""
        res = self.client.get(CREATE_RETRIEVE_UPDATE_TEACHER_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.user_teacher))
        self.assertEqual(res.data['teacher_profile']['first_name'], '')
        self.assertEqual(res.data['teacher_profile']['last_name'], '')
        self.assertEqual(res.data['teacher_profile']['phone'], None)
        self.assertEqual(res.data['teacher_profile']['gender'], '')
        self.assertEqual(res.data['teacher_profile']['country'], 'IN')
        self.assertEqual(res.data['teacher_profile']['date_of_birth'], None)
        self.assertIn('created_date', res.data)
        self.assertEqual(res.data['username'], 'testuser')
        self.assertEqual(res.data['teacher_profile']['primary_language'],
                         models.Languages.ENGLISH)
        self.assertEqual(res.data['teacher_profile']
                         ['secondary_language'], None)
        self.assertEqual(res.data['teacher_profile']
                         ['tertiary_language'], None)

    def test_update_successful_authorized_teacher(self):
        """Test that authenticated teacher can see their profile details"""
        payload = {
            'username': 'changedusername',
            'teacher_profile': {
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

        res = self.client.patch(CREATE_RETRIEVE_UPDATE_TEACHER_PROFILE_URL,
                                payload, format='json')
        res_profile = dict(res.data['teacher_profile'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], str(self.user_teacher))
        self.assertEqual(res.data['username'], payload['username'])
        self.assertEqual(res_profile['first_name'],
                         payload['teacher_profile']['first_name'].upper())
        self.assertEqual(res_profile['last_name'],
                         payload['teacher_profile']['last_name'].upper())
        self.assertEqual(res_profile['phone'],
                         payload['teacher_profile']['phone'])
        self.assertEqual(res_profile['gender'],
                         payload['teacher_profile']['gender'])
        self.assertEqual(res_profile['country'],
                         payload['teacher_profile']['country'])
        self.assertEqual(res_profile['date_of_birth'],
                         payload['teacher_profile']['date_of_birth'])
        self.assertIn('created_date', res.data)
        self.assertEqual(res_profile['primary_language'],
                         payload['teacher_profile']['primary_language'])
        self.assertEqual(res_profile['secondary_language'],
                         payload['teacher_profile']['secondary_language'])
        self.assertEqual(res_profile['tertiary_language'], None)

    def test_post_create_retrieve_update_not_allowed(self):
        """Test that post is not allowed on create retrieve update url"""
        res = self.client.post(CREATE_RETRIEVE_UPDATE_TEACHER_PROFILE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
#         self.teacher_user.teacher_profile.image.delete()

#     def test_teacher_profile_picture_upload(self):
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
