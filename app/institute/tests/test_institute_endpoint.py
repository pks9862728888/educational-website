from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

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


def get_invite_url(slug_text):
    """Creates and returns institute permission add url"""
    return reverse("institute:provide_permission",
                   kwargs={'institute_slug': slug_text})


def get_invite_accept_delete_url(slug_text):
    """Creates and returns institute permission accept delete url"""
    return reverse("institute:accept_delete_permission",
                   kwargs={'institute_slug': slug_text})


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


def create_institute(user, institute_name='tempinstitute'):
    """Creates institute and return institute"""
    return models.Institute.objects.create(
        name=institute_name,
        user=user,
        institute_category=models.InstituteCategory.EDUCATION
    )


def create_invite(institute, inviter, invitee, role):
    """Creates and returns institute invite permission"""
    return models.InstitutePermission.objects.create(
        institute=institute,
        inviter=inviter,
        invitee=invitee,
        role=role
    )


def accept_invite(institute, invitee, role):
    """Accepts the permission"""
    role = models.InstitutePermission.objects.filter(
        institute=institute,
        invitee=invitee,
        role=role
    ).first()
    role.active = True
    role.request_accepted_on = timezone.now()
    role.save()


def delete_invite(institute, invitee, role):
    """Accepts the permission"""
    role = models.InstitutePermission.objects.filter(
        institute=institute,
        invitee=invitee,
        role=role
    ).first()
    role.delete()


def role_exists(institute, inviter, invitee, role, active=True):
    """Returns whether role exists or not"""
    return models.InstitutePermission.objects.filter(
        institute=institute,
        inviter=inviter,
        invitee=invitee,
        role=role,
        active=active
    ).exists()


# class PublicInstituteApiTests(TestCase):
#     """Tests the institute api for unauthenticated user"""
#
#     def setUp(self):
#         """Setup code for all test cases"""
#         self.user = get_user_model().objects.create_user(
#             email='test@gmail.com',
#             username='testusername',
#             password='testpassword',
#             is_teacher=True
#         )
#         self.client = APIClient()
#
#     def test_get_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that get request is not allowed for unauthenticated user"""
#         res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_post_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that post is not allowed for unauthenticated user"""
#         res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
#             "user": self.user,
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_get_not_allowed_on_institute_create_url(self):
#         """Test that get request is not allowed for unauthenticated user"""
#         res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_post_not_allowed_on_institute_create_teacher_url(self):
#         """Test that post is not allowed for unauthenticated user"""
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def get_not_allowed_on_institute_full_details_url(self):
#         """Test that get is not allowed for unauthenticated user"""
#         teacher_user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             password='temppassword',
#             username='tempusername',
#             is_teacher=True
#         )
#         institute = models.Institute.objects.create(
#             user=teacher_user,
#             name='temp name',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.post(get_full_details_institute_url(
#             institute.institute_slug))
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


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

    # def test_get_success_institute_min_endpoint_teacher(self):
    #     """Test that get request is success for teacher"""
    #     payload = {
    #         'name': 'Temp Institute',
    #         'institute_category': models.InstituteCategory.EDUCATION,
    #         'country': 'US',
    #         'institute_profile': {
    #             'motto': 'Sample motto',
    #             'email': 'abc@gmail.com',
    #             'phone': '+919878787878',
    #             'website_url': 'www.google.com',
    #             'recognition': 'ICSE',
    #             'state': models.StatesAndUnionTerritories.ASSAM
    #         }
    #     }
    #     institute = models.Institute.objects.create(
    #         user=self.user,
    #         name=payload['name'],
    #         country=payload['country'],
    #         institute_category=payload['institute_category']
    #     )
    #     institute_profile = payload['institute_profile']
    #     institute.institute_profile.motto = institute_profile['motto']
    #     institute.institute_profile.email = institute_profile['email']
    #     institute.institute_profile.phone = institute_profile['phone']
    #     institute.institute_profile.website_url = institute_profile[
    #         'website_url']
    #     institute.institute_profile.recognition = institute_profile[
    #         'recognition']
    #     institute.institute_profile.state = institute_profile['state']
    #     institute.save()
    #
    #     res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     self.assertEqual(res.data[0]['user'], self.user.pk)
    #     self.assertIn('institute_slug', res.data[0])
    #     self.assertEqual(res.data[0]['name'], payload['name'].lower())
    #     self.assertEqual(res.data[0]['institute_category'],
    #                      payload['institute_category'])
    #     self.assertEqual(res.data[0]['country'], payload['country'])
    #     self.assertEqual(res.data[0]['institute_profile']['motto'],
    #                      payload['institute_profile']['motto'])
    #     self.assertEqual(res.data[0]['institute_profile']['email'],
    #                      payload['institute_profile']['email'])
    #     self.assertEqual(res.data[0]['institute_profile']['phone'],
    #                      payload['institute_profile']['phone'])
    #     self.assertEqual(res.data[0]['institute_profile']['website_url'],
    #                      payload['institute_profile']['website_url'])
    #     self.assertEqual(res.data[0]['institute_profile']['recognition'],
    #                      payload['institute_profile']['recognition'])
    #     self.assertEqual(res.data[0]['institute_profile']['state'],
    #                      payload['institute_profile']['state'])
    #     self.assertEqual(list(res.data[0]['institute_logo']), [])
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_students'], 0)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_faculties'], 0)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_staff'], 0)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_admin'], 1)
    #
    # def test_get_statistics_on_institute_min_endpoint_teacher_success(self):
    #     """Test that get request is success for teacher"""
    #     institute = create_institute(self.user)
    #     admin1 = create_teacher('admindfds@gaail.com', 'adminsdf')
    #     staff1 = create_teacher('staffd@gmail.com', 'abcdkfjj')
    #     staff2 = create_teacher('staffdfdd@gmail.com', 'sdfsdfd')
    #     faculty1 = create_teacher('facultysdfsf@gmail.com', 'sfdsdfsqwe')
    #     faculty2 = create_teacher('facultysdsfsf@gmail.com', 'sfdsssdfsqwe')
    #
    #     create_invite(institute, self.user, admin1, models.InstituteRole.ADMIN)
    #     create_invite(institute, self.user, staff1, models.InstituteRole.STAFF)
    #     create_invite(institute, self.user, staff2, models.InstituteRole.STAFF)
    #     create_invite(institute, self.user, faculty1, models.InstituteRole.FACULTY)
    #     create_invite(institute, self.user, faculty2, models.InstituteRole.FACULTY)
    #
    #     accept_invite(institute, admin1, models.InstituteRole.ADMIN)
    #     accept_invite(institute, staff1, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff2, models.InstituteRole.STAFF)
    #     accept_invite(institute, faculty1, models.InstituteRole.FACULTY)
    #
    #     res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_students'], 0)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_faculties'], 1)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_staff'], 2)
    #     self.assertEqual(res.data[0]['institute_statistics']['no_of_admin'], 2)

#     def test_get_other_institute_fail_institute_min_endpoint_teacher(self):
#         """Test that un-enrolled institute can not be get by teacher"""
#         models.Institute.objects.create(
#             user=self.user,
#             name='Temp Institute',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         models.Institute.objects.create(
#             user=create_teacher(),
#             name='Temp Institute',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#
#     def test_post_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that post is not allowed for authenticated teacher"""
#         res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
#             "user": self.user,
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_create_institute_success_by_teacher(self):
#         """Test that creating an institute with valid details is success"""
#         payload = {
#             'name': 'Name of institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'IN',
#             'institute_profile': {
#                 'motto': '',
#                 'email': '',
#                 'phone': '',
#                 'website_url': '',
#                 'recognition': '',
#                 'state': '',
#                 'pin': '',
#                 'address': '',
#                 'primary_language': models.Languages.ENGLISH,
#                 'secondary_language': '',
#                 'tertiary_language': ''
#             }
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL,
#                                payload, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(res.data['created'], 'true')
#         self.assertIn('url', res.data)
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#
#         institute = models.Institute.objects.get(
#             name=payload['name'].lower())
#         institute_profile = models.InstituteProfile.objects.get(
#             institute=institute)
#         self.assertEqual(institute.name, payload['name'].lower())
#         self.assertEqual(institute.country, payload['country'])
#         self.assertEqual(institute.institute_category,
#                          payload['institute_category'])
#         self.assertEqual(institute_profile.motto,
#                          payload['institute_profile']['motto'])
#         self.assertEqual(institute_profile.email,
#                          payload['institute_profile']['email'])
#         self.assertEqual(institute_profile.phone,
#                          payload['institute_profile']['phone'])
#         self.assertEqual(institute_profile.website_url,
#                          payload['institute_profile']['website_url'])
#         self.assertEqual(institute_profile.recognition,
#                          payload['institute_profile']['recognition'])
#         self.assertEqual(institute_profile.state,
#                          payload['institute_profile']['state'])
#         self.assertEqual(institute_profile.pin,
#                          payload['institute_profile']['pin'])
#         self.assertEqual(institute_profile.address,
#                          payload['institute_profile']['address'])
#         self.assertEqual(institute_profile.primary_language,
#                          payload['institute_profile']['primary_language'])
#         self.assertEqual(institute_profile.secondary_language,
#                          payload['institute_profile']['secondary_language'])
#         self.assertEqual(institute_profile.tertiary_language,
#                          payload['institute_profile']['tertiary_language'])
#
#     def test_create_institute_full_details_success_by_teacher(self):
#         """
#         Test that creating an institute with
#         full valid details is success
#         """
#         payload = {
#             'name': 'Temp Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US',
#             'institute_profile': {
#                 'motto': 'Sample motto',
#                 'email': 'abc@gmail.com',
#                 'phone': '+919878787878',
#                 'website_url': 'http://www.google.com',
#                 'recognition': 'ICSE',
#                 'state': models.StatesAndUnionTerritories.ASSAM,
#                 'pin': '799878',
#                 'address': 'Dadra and nagar haveli, west district',
#                 'primary_language': models.Languages.HINDI,
#                 'secondary_language': models.Languages.ENGLISH,
#                 'tertiary_language': ''
#             }
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL,
#                                payload, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(res.data['created'], 'true')
#         self.assertIn('url', res.data)
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#
#         institute = models.Institute.objects.get(
#             name=payload['name'].lower())
#         institute_profile = models.InstituteProfile.objects.get(
#             institute=institute)
#
#         self.assertEqual(institute.name, payload['name'].lower())
#         self.assertEqual(institute.country, payload['country'])
#         self.assertEqual(institute.institute_category,
#                          payload['institute_category'])
#         self.assertEqual(institute_profile.motto,
#                          payload['institute_profile']['motto'])
#         self.assertEqual(institute_profile.email,
#                          payload['institute_profile']['email'])
#         self.assertEqual(institute_profile.phone,
#                          payload['institute_profile']['phone'])
#         self.assertEqual(institute_profile.website_url,
#                          payload['institute_profile']['website_url'])
#         self.assertEqual(institute_profile.recognition,
#                          payload['institute_profile']['recognition'])
#         self.assertEqual(institute_profile.state,
#                          payload['institute_profile']['state'])
#         self.assertEqual(institute_profile.pin,
#                          payload['institute_profile']['pin'])
#         self.assertEqual(institute_profile.address,
#                          payload['institute_profile']['address'])
#         self.assertEqual(institute_profile.primary_language,
#                          payload['institute_profile']['primary_language'])
#         self.assertEqual(institute_profile.secondary_language,
#                          payload['institute_profile']['secondary_language'])
#         self.assertEqual(institute_profile.tertiary_language,
#                          payload['institute_profile']['tertiary_language'])
#
#     def test_create_institute_name_required(self):
#         """Test that creating institute with invalid details fails"""
#         payload = {
#             'name': '   ',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US'
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(models.Institute.objects.filter(
#             user=self.user).exists())
#
#     def test_institute_category_required(self):
#         """Test that institute_category is required to create institute"""
#         payload = {
#             'name': '   ',
#             'institute_category': '',
#             'country': 'US'
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_institute_creation_fails_invalid_data(self):
#         """Test that institute_category is required to create institute"""
#         payload = {
#             'name': 'test oomm',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US',
#             'institute_profile': {
#                 'motto': 'Sample motto',
#                 'email': 'gmail.com',
#                 'phone': '78787878',
#                 'website_url': 'www.google.com'
#             }
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#
#     def test_create_institute_in_other_teacher_name_fails(self):
#         """Test that teacher can create institute in his name only"""
#         new_user = create_teacher()
#         payload = {
#             'user': new_user,
#             'name': '   ',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US'
#         }
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(models.Institute.objects.filter(
#             user=new_user).exists())
#         self.assertFalse(models.Institute.objects.filter(
#             user=self.user).exists())
#
#     def test_duplicate_institute_fails(self):
#         """Test that teacher can not create a duplicate institute"""
#         payload = {
#             'name': '   ',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US'
#         }
#         self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, **payload)
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_get_success_on_institute_full_details_url(self):
#         """Test that teacher can get full details of institute"""
#         institute = models.Institute.objects.create(
#             user=self.user,
#             name='temp institute',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#
#         res = self.client.get(get_full_details_institute_url(
#             institute.institute_slug))
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['name'], 'temp institute')
#         self.assertIn('institute_profile', res.data)
#         self.assertIn('institute_logo', res.data)
#         self.assertIn('institute_banner', res.data)
#
#     def test_invite_admin_success_by_owner_admin(self):
#         """Invite success by owner admin"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         ).exists())
#
#     def test_invite_admin_success_by_active_admin(self):
#         """Invite success by active admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         perm.active = True
#         perm.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         ).exists())
#
#     def test_invite_admin_fails_by_inactive_admin(self):
#         """Invite fails by inactive admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         ).exists())
#
#     def test_invite_admin_fails_by_non_admin(self):
#         """Invite fails by non admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         ).exists())
#
#     def test_duplicate_invite_admin_fails(self):
#         """Re-inviting user as admin fails"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'], 'User already invited.')
#         self.assertEqual(len(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         )), 1)
#
#     def test_invite_student_as_admin_fails(self):
#         """Invite fails for providing admin permission to student"""
#         institute = create_institute(self.user)
#         student = create_student()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': str(student)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'],
#                          'Only teacher user can be assigned special roles.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=student,
#             role=models.InstituteRole.ADMIN,
#             active=False
#         ))
#
#     def test_invite_role_invitee_required(self):
#         """Invite fails if role and invitee are not provided"""
#         institute = create_institute(self.user)
#
#         res = self.client.post(get_invite_url(institute.institute_slug), {})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['role'], 'This field is required.')
#         self.assertEqual(res.data['invitee'], 'This field is required.')
#
#     def test_invite_fails_for_wrong_invitee(self):
#         """Invite fails if invitee does not exist"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.ADMIN, 'invitee': 'abcddf@gmail.com'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'], 'This user does not exist.')
#
#     def test_invite_staff_success_by_owner_admin(self):
#         """Invite success by owner admin"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_staff_success_by_active_admin(self):
#         """Invite success by active admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         staff = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         perm.active = True
#         perm.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=staff,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_staff_fails_by_inactive_admin(self):
#         """Invite fails by inactive admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_staff_fails_by_non_admin(self):
#         """Invite fails by non admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         staff = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=staff,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_staff_fails_by_inactive_staff(self):
#         """Invite fails by inactive staff"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_staff_fails_by_active_staff(self):
#         """Invite fails by active staff"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         perm.active = True
#         perm.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_duplicate_invite_staff_fails(self):
#         """Invite fails for multiple invite for staff role"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'], 'User already invited.')
#         self.assertEqual(len(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         )), 1)
#
#     def test_invite_student_as_staff_fails(self):
#         """Invite fails if student user are invited as staff"""
#         institute = create_institute(self.user)
#         student = create_student()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.STAFF, 'invitee': str(student)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'],
#                          'Only teacher user can be assigned special roles.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=student,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ))
#
#     def test_invite_faculty_success_by_owner_admin(self):
#         """Invite success by owner admin"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ).exists())
#
#     def test_invite_faculty_success_by_active_admin(self):
#         """Invite success by active admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         faculty = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         perm.active = True
#         perm.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=faculty,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ).exists())
#
#     def test_invite_faculty_fails_by_inactive_admin(self):
#         """Invite fails by inactive admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_faculty_fails_by_inactive_staff(self):
#         """Invite fails by inactive staff"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.STAFF,
#             active=False
#         ).exists())
#
#     def test_invite_faculty_success_by_active_staff(self):
#         """Invite success by active staff"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         faculty = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         perm.active = True
#         perm.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'INVITED')
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=faculty,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ).exists())
#
#     def test_invite_faculty_fails_by_non_admin(self):
#         """Invite fails by non admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         faculty = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=faculty,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ).exists())
#
#     def test_duplicate_invite_faculty_fails(self):
#         """Invite fails for multiple invite for faculty role"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.FACULTY
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'], 'User already invited.')
#         self.assertEqual(len(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         )), 1)
#
#     def test_invite_student_as_faculty_fails(self):
#         """Invite fails if student user are invited as faculty"""
#         institute = create_institute(self.user)
#         student = create_student()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(student)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['invitee'],
#                          'Only teacher user can be assigned special roles.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=student,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ))
#
#     def test_invite_faculty_fails_by_inactive_faculty(self):
#         """Invite fails if inactive faculty tries to invite faculty"""
#         owner = create_teacher('ownersd@gmail.com', 'owenerfd')
#         institute = create_institute(owner)
#         teacher = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.FACULTY
#         )
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ))
#
#     def test_invite_faculty_fails_by_active_faculty(self):
#         """Invite fails if active faculty tries to invite faculty"""
#         owner = create_teacher('ownersd@gmail.com', 'owenerfd')
#         institute = create_institute(owner)
#         teacher = create_teacher()
#         role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.FACULTY
#         )
#         role.active = True
#         role.save()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': models.InstituteRole.FACULTY, 'invitee': str(teacher)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertFalse(models.InstitutePermission.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.FACULTY,
#             active=False
#         ))
#
#     def test_invite_fails_invalid_role(self):
#         """Invite fails by non admin"""
#         admin = create_teacher('admindf@gmail.com', 'adminsdf')
#         institute = create_institute(admin)
#         staff = create_teacher()
#
#         res = self.client.post(
#             get_invite_url(institute.institute_slug),
#             {'role': 'B', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['role'], 'Invalid role.')
#
#     def test_invitee_can_accept_admin_request(self):
#         """Test that invitee can accept admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.ADMIN))
#
#     def test_invitee_can_accept_staff_request(self):
#         """Test that invitee can accept staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.STAFF))
#
#     def test_invitee_can_accept_faculty_request(self):
#         """Test that invitee can accept faculty request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.FACULTY))
#
#     def test_invitee_can_accept_admin_request_twice(self):
#         """Test that invitee can not accept admin request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#         accept_invite(institute, self.user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Join request already accepted.')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.ADMIN))
#
#     def test_invitee_can_accept_staff_request_twice(self):
#         """Test that invitee can not accept staff request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.STAFF)
#         accept_invite(institute, self.user,
#                       models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Join request already accepted.')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.STAFF))
#
#     def test_invitee_can_accept_faculty_request_twice(self):
#         """Test that invitee can not accept faculty request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         accept_invite(institute, self.user,
#                       models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Join request already accepted.')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.FACULTY))
#
#     def test_inviter_can_not_accept_request_of_invitee(self):
#         """Test that inviter can not accept request of invitee"""
#         invitee = create_teacher()
#         institute = create_institute(self.user)
#         create_invite(institute, self.user, invitee,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Join request already accepted.')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.ADMIN))
#
#     def test_operation_required_for_accept(self):
#         """Test that operation is required to accept role"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['operation'],
#                          'This field is required.')
#         self.assertTrue(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_invitee_can_delete_admin_request(self):
#         """Test that invitee can delete admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_invitee_can_delete_staff_request(self):
#         """Test that invitee can delete staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_invitee_can_decline_faculty_request(self):
#         """Test that invitee can delete faculty request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.FACULTY, False))
#
#     def test_invitee_can_not_delete_admin_request_twice(self):
#         """Test that invitee can not delete admin request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#         delete_invite(institute, self.user,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_invitee_can_not_delete_staff_request_twice(self):
#         """Test that invitee can not delete staff request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.STAFF)
#         delete_invite(institute, self.user,
#                       models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_invitee_can_not_delete_faculty_request_twice(self):
#         """Test that invitee can not delete faculty request twice"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         delete_invite(institute, self.user,
#                       models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, owner, self.user,
#                         models.InstituteRole.FACULTY, False))
#
#     def test_inviter_can_decline_admin_request(self):
#         """Test that inviter can delete admin request"""
#         invitee = create_teacher()
#         institute = create_institute(self.user)
#         create_invite(institute, self.user, invitee,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_other_active_admin_can_decline_admin_request(self):
#         """Test that all active admin can delete admin request"""
#         invitee = create_teacher()
#         owner = create_teacher('ownerdf@gmail.com', 'owenrdf')
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#         accept_invite(institute, self.user,
#                       models.InstituteRole.ADMIN)
#         create_invite(institute, owner, invitee,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_other_inactive_admin_can_not_decline_admin_request(self):
#         """Test that inactive admin can not delete admin request"""
#         invitee = create_teacher()
#         owner = create_teacher('ownerdf@gmail.com', 'owenrdf')
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.ADMIN)
#         create_invite(institute, owner, invitee,
#                       models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, invitee,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_inviter_can_decline_staff_request(self):
#         """Test that inviter can delete staff request"""
#         invitee = create_teacher()
#         institute = create_institute(self.user)
#         create_invite(institute, self.user, invitee,
#                       models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.STAFF, False))
#
#     def test_inviter_can_decline_faculty_request(self):
#         """Test that inviter can delete faculty request"""
#         invitee = create_teacher()
#         institute = create_institute(self.user)
#         create_invite(institute, self.user, invitee,
#                       models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.FACULTY, False))
#
#     def test_inviter_can_delete_admin_request_twice(self):
#         """Test that inviter can not delete admin request twice"""
#         institute = create_institute(self.user)
#         new_user = create_teacher()
#         create_invite(institute, self.user, new_user,
#                       models.InstituteRole.ADMIN)
#         delete_invite(institute, new_user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, new_user, self.user,
#                         models.InstituteRole.ADMIN))
#
#     def test_inviter_can_not_delete_staff_request_twice(self):
#         """Test that inviter can not delete staff request twice"""
#         institute = create_institute(self.user)
#         new_user = create_teacher()
#         create_invite(institute, self.user, new_user,
#                       models.InstituteRole.STAFF)
#         delete_invite(institute, new_user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, new_user, self.user,
#                         models.InstituteRole.STAFF))
#
#     def test_inviter_can_not_delete_faculty_request_twice(self):
#         """Test that inviter can not delete faculty request twice"""
#         institute = create_institute(self.user)
#         new_user = create_teacher()
#         create_invite(institute, self.user, new_user,
#                       models.InstituteRole.FACULTY)
#         delete_invite(institute, new_user, models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, new_user, self.user,
#                         models.InstituteRole.FACULTY))
#
#     def test_inviter_can_not_decline_non_existing_admin_request(self):
#         """Test that inviter can delete non existing admin request"""
#         invitee = create_teacher()
#         institute = create_institute(self.user)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'],
#                          'Invitation not found or already deleted.')
#         self.assertFalse(
#             role_exists(institute, self.user, invitee,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_active_staff_can_not_delete_admin_request(self):
#         """Test that active staff can not delete admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user, models.InstituteRole.STAFF)
#         accept_invite(institute, self.user, models.InstituteRole.STAFF)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_inactive_staff_can_not_delete_admin_request(self):
#         """Test that inactive staff can not delete admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user, models.InstituteRole.STAFF)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_active_faculty_can_not_delete_admin_request(self):
#         """Test that active faculty can not delete admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         accept_invite(institute, self.user, models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_inactive_faculty_can_not_delete_admin_request(self):
#         """Test that inactive faculty can not delete admin request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_active_faculty_can_not_delete_staff_request(self):
#         """Test that active faculty can not delete staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         accept_invite(institute, self.user, models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_inactive_faculty_can_not_delete_staff_request(self):
#         """Test that inactive faculty can not delete staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_active_staff_can_not_delete_staff_request(self):
#         """Test that active staff can not delete staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user, models.InstituteRole.STAFF)
#         accept_invite(institute, self.user, models.InstituteRole.STAFF)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_inactive_staff_can_not_delete_staff_request(self):
#         """Test that inactive staff can not delete staff request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user, models.InstituteRole.STAFF)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.STAFF, False))
#
#     def test_active_faculty_can_not_delete_faculty_request(self):
#         """Test that active faculty can not delete faculty request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         accept_invite(institute, self.user, models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.FACULTY, False))
#
#     def test_inactive_faculty_can_not_delete_faculty_request(self):
#         """Test that inactive faculty can not delete faculty request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         create_invite(institute, owner, self.user,
#                       models.InstituteRole.FACULTY)
#         new_user = create_teacher('newuser@gmail.com', 'newusersfddff')
#         create_invite(institute, owner, new_user, models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, new_user,
#                         models.InstituteRole.FACULTY, False))
#
#     def test_active_admin_can_not_remove_active_admin(self):
#         """Test that active admin can not remove active admin"""
#         institute = create_institute(self.user)
#         admin = create_teacher()
#         create_invite(institute, self.user, admin, models.InstituteRole.ADMIN)
#         accept_invite(institute, admin, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(admin)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, self.user, admin,
#                         models.InstituteRole.ADMIN, True))
#
#     def test_active_admin_can_remove_inactive_admin(self):
#         """Test that active admin can not remove inactive admin"""
#         institute = create_institute(self.user)
#         admin = create_teacher()
#         create_invite(institute, self.user, admin, models.InstituteRole.ADMIN)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(admin)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(
#             role_exists(institute, self.user, admin,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_active_staff_can_not_remove_active_staff(self):
#         """Test that active staff can not remove active staff"""
#         admin = create_teacher('activeadmin@gmail.com', 'activeadminfd')
#         institute = create_institute(admin)
#         staff = create_teacher()
#         create_invite(institute, admin, staff, models.InstituteRole.STAFF)
#         accept_invite(institute, staff, models.InstituteRole.STAFF)
#         create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
#         accept_invite(institute, self.user, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, admin, staff,
#                         models.InstituteRole.STAFF, True))
#
#     def test_active_faculty_can_not_remove_active_staff(self):
#         """Test that active faculty can not remove active faculty"""
#         admin = create_teacher('activeadmin@gmail.com', 'activeadminfd')
#         institute = create_institute(admin)
#         faculty = create_teacher()
#         create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
#         accept_invite(institute, faculty, models.InstituteRole.FACULTY)
#         create_invite(institute, admin, self.user,
#                       models.InstituteRole.FACULTY)
#         accept_invite(institute, self.user, models.InstituteRole.FACULTY)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, admin, faculty,
#                         models.InstituteRole.FACULTY, True))
#
#     def test_active_admin_can_not_delete_other_institute_admin_request(self):
#         """
#         Test that all active admin can not delete
#         admin request of other institute
#         """
#         invitee = create_teacher()
#         owner = create_teacher('ownerdf@gmail.com', 'owenrdf')
#         institute = create_institute(owner)
#         create_invite(institute, owner, invitee, models.InstituteRole.ADMIN)
#         create_institute(self.user, 'Billy institute')
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(invitee)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Permission denied.')
#         self.assertTrue(
#             role_exists(institute, owner, invitee,
#                         models.InstituteRole.ADMIN, False))
#
#     def test_admin_can_not_delete_active_staff_using_this_url(self):
#         """
#         Test active admin can not delete active
#         staff using accept delete url"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
#         accept_invite(institute, staff, models.InstituteRole.STAFF)
#
#         res = self.client.post(
#             get_invite_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code,
#                          status.HTTP_500_INTERNAL_SERVER_ERROR)
#         self.assertEqual(res.data['error'],
#                          'Internal server error. Please contact EduWeb.')
#         self.assertTrue(
#             role_exists(institute, self.user, staff,
#                         models.InstituteRole.STAFF, True))
#
#
# class AuthenticatedStudentUserAPITests(TestCase):
#     """Tests for authenticated student user"""
#
#     def setUp(self):
#         """Setup code for all test cases"""
#         self.user = get_user_model().objects.create_user(
#             email='test@gmail.com',
#             username='testusername',
#             password='testpassword',
#             is_student=True
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_get_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that get request is not allowed for unauthenticated user"""
#         res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_post_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that post is not allowed for unauthenticated user"""
#         res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
#             "user": self.user,
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_not_allowed_on_institute_create_url(self):
#         """Test that get request is not allowed for student user"""
#         res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_post_not_allowed_on_institute_create_url(self):
#         """Test that post is not allowed for student user"""
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def get_not_allowed_on_institute_full_details_url(self):
#         """Test that get is not allowed for student user"""
#         teacher_user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             password='temppassword',
#             username='tempusername',
#             is_teacher=True
#         )
#         institute = models.Institute.objects.create(
#             user=teacher_user,
#             name='temp name',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.post(
#             get_full_details_institute_url(institute.institute_slug))
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_not_allowed_on_institute_admin_add_url_by_student(self):
#         """
#         Test that get is not allowed by student
#         on institute admin add url
#         """
#         teacher = create_teacher()
#         institute = models.Institute.objects.create(
#             user=teacher,
#             name='Whatever whatever',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.get(get_invite_url(institute.institute_slug))
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_add_admin_failure_by_student(self):
#         """Test that student can't add other admin"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         institute_slug = institute.institute_slug
#         payload = {
#             'email': 'sdfsdf@gmail.com',
#             'username': 'abctsdfsempuser'
#         }
#         create_teacher(payload['email'], payload['username'])
#         res = self.client.post(
#             get_invite_url(institute_slug), {
#                 'email': payload['email'],
#                 'institute_slug': institute_slug
#             })
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class AuthenticatedUserAPITests(TestCase):
#     """Tests for authenticated user"""
#
#     def setUp(self):
#         """Setup code for all test cases"""
#         self.user = get_user_model().objects.create_user(
#             email='test@gmail.com',
#             username='testusername',
#             password='testpassword',
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_get_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that get request is not allowed for unauthenticated user"""
#         res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_post_not_allowed_on_institute_min_details_teacher_url(self):
#         """Test that post is not allowed for unauthenticated user"""
#         res = self.client.post(INSTITUTE_MIN_DETAILS_TEACHER_URL, {
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_not_allowed_on_institute_create_url(self):
#         """Test that get request is not allowed for staff user"""
#         res = self.client.get(INSTITUTE_CREATE_BY_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_post_not_allowed_on_institute_create_url(self):
#         """Test that post is not allowed for staff user"""
#         res = self.client.post(INSTITUTE_CREATE_BY_TEACHER_URL, {
#             "name": "Temp name",
#             "institute_category": models.InstituteCategory.EDUCATION
#         })
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def get_not_allowed_on_institute_full_details_url(self):
#         """Test that get is not allowed for normal authenticated user"""
#         teacher_user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             password='temppassword',
#             username='tempusername',
#             is_teacher=True
#         )
#         institute = models.Institute.objects.create(
#             user=teacher_user,
#             name='temp name',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.post(
#             get_full_details_institute_url(institute.institute_slug))
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_not_allowed_on_institute_admin_add_url_by_user(self):
#         """Test that get is not allowed by user on institute admin add url"""
#         teacher_user = create_teacher()
#         institute = models.Institute.objects.create(
#             user=teacher_user,
#             name='Whatever whatever',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.get(get_invite_url(institute.institute_slug))
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_add_admin_failure_by_authenticated_normal_user(self):
#         """Test that authenticated normal user can't add other admin"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         institute_slug = institute.institute_slug
#         payload = {
#             'email': 'abc12@gmail.com',
#             'username': 'abc23tempuser'
#         }
#         create_teacher(payload['email'], payload['username'])
#         res = self.client.post(
#             get_invite_url(institute_slug), {
#                 'email': payload['email'],
#                 'role': models.InstituteRole.ADMIN
#             })
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
