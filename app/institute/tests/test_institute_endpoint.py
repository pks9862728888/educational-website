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


def get_admin_add_url(slug_text):
    """Creates and returns admin add url"""
    return reverse("institute:request_for_admin",
                   kwargs={'institute_slug': slug_text})


def get_staff_add_url(slug_text):
    """Creates and returns staff add url"""
    return reverse("institute:request_for_staff",
                   kwargs={'institute_slug': slug_text})


def get_faculty_add_url(slug_text):
    """Creates and returns faculty add url"""
    return reverse("institute:request_for_faculty",
                   kwargs={'institute_slug': slug_text})


def get_admin_accept_delete_url(slug_text):
    """Creates and returns admin request accept or detail url"""
    return reverse("institute:accept_delete_admin_request",
                   kwargs={'institute_slug': slug_text})


def get_staff_accept_delete_url(slug_text):
    """Creates and returns staff request accept or detail url"""
    return reverse("institute:accept_delete_staff_request",
                   kwargs={'institute_slug': slug_text})


def get_faculty_accept_delete_url(slug_text):
    """Creates and returns staff request accept or detail url"""
    return reverse("institute:accept_delete_faculty_request",
                   kwargs={'institute_slug': slug_text})


def create_teacher(email='abc@gmail.com', username='tempusername'):
    """Creates and return teacher"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_teacher=True
    )


def create_institute(user, institute_name='tempinstitute'):
    """Creates institute and return institute"""
    return models.Institute.objects.create(
        name=institute_name,
        user=user,
        institute_category=models.InstituteCategory.EDUCATION
    )


def create_student(email='abc@gmail.com', username='tempusername'):
    """Creates and return student"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_student=True
    )


def add_staff_role(inviter, invitee, institute, active=False):
    """Creates and returns institute staff"""
    return models.InstituteStaff.objects.create(
        inviter=inviter,
        invitee=invitee,
        institute=institute,
        active=active
    )


def add_faculty_role(inviter, invitee, institute, active=False):
    """Creates and returns institute faculty"""
    return models.InstituteFaculty.objects.create(
        inviter=inviter,
        invitee=invitee,
        institute=institute,
        active=active
    )


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
#
#     def get_not_allowed_on_institute_admin_add_url(self):
#         """Test that get is not allowed on institute admin add url"""
#         teacher = create_teacher()
#         institute = models.Institute.objects.create(
#             user=teacher,
#             name='Whatever whatever',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.get(get_admin_add_url(institute.institute_slug))
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


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

#     def test_get_success_institute_min_endpoint_teacher(self):
#         """Test that get request is success for teacher"""
#         payload = {
#             'name': 'Temp Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'country': 'US',
#             'institute_profile': {
#                 'motto': 'Sample motto',
#                 'email': 'abc@gmail.com',
#                 'phone': '+919878787878',
#                 'website_url': 'www.google.com',
#                 'recognition': 'ICSE',
#                 'state': models.StatesAndUnionTerritories.ASSAM
#             }
#         }
#         institute = models.Institute.objects.create(
#             user=self.user,
#             name=payload['name'],
#             country=payload['country'],
#             institute_category=payload['institute_category']
#         )
#         institute_profile = payload['institute_profile']
#         institute.institute_profile.motto = institute_profile['motto']
#         institute.institute_profile.email = institute_profile['email']
#         institute.institute_profile.phone = institute_profile['phone']
#         institute.institute_profile.website_url = institute_profile[
#             'website_url']
#         institute.institute_profile.recognition = institute_profile[
#             'recognition']
#         institute.institute_profile.state = institute_profile['state']
#         institute.save()
#
#         res = self.client.get(INSTITUTE_MIN_DETAILS_TEACHER_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#         self.assertEqual(res.data[0]['user'], self.user.pk)
#         self.assertIn('institute_slug', res.data[0])
#         self.assertEqual(res.data[0]['name'], payload['name'].lower())
#         self.assertEqual(res.data[0]['institute_category'],
#                          payload['institute_category'])
#         self.assertEqual(res.data[0]['country'], payload['country'])
#         self.assertEqual(res.data[0]['institute_profile']['motto'],
#                          payload['institute_profile']['motto'])
#         self.assertEqual(res.data[0]['institute_profile']['email'],
#                          payload['institute_profile']['email'])
#         self.assertEqual(res.data[0]['institute_profile']['phone'],
#                          payload['institute_profile']['phone'])
#         self.assertEqual(res.data[0]['institute_profile']['website_url'],
#                          payload['institute_profile']['website_url'])
#         self.assertEqual(res.data[0]['institute_profile']['recognition'],
#                          payload['institute_profile']['recognition'])
#         self.assertEqual(res.data[0]['institute_profile']['state'],
#                          payload['institute_profile']['state'])
#         self.assertEqual(list(res.data[0]['institute_logo']), [])
#
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
    # def test_get_not_allowed_on_institute_admin_add_url(self):
    #     """
    #     Test that get is not allowed by teacher
    #     on institute admin add url
    #     """
    #     institute = create_institute(self.user)
    #     res = self.client.get(get_admin_add_url(institute.institute_slug))
    #     self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    #
    # def test_add_admin_success_by_owner_admin(self):
    #     """Test that owner admin can add another admin"""
    #     institute = create_institute(self.user, 'EmilyInstitute')
    #     payload = {
    #         'email': 'horibol@gmail.com',
    #         'username': 'abcdftesdfsfmpuser'
    #     }
    #     create_teacher(
    #         email=payload['email'],
    #         username=payload['username']
    #     )
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': payload['email']
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['requested'], 'True')
    #
    # def test_add_admin_failure_by_other_teacher(self):
    #     """Test that non-admin can't add other admin"""
    #     owner = create_teacher('ubicutous@gmail.com', 'ubicutorus')
    #     institute = create_institute(owner, 'Sample institute')
    #     payload = {
    #         'email': 'inviteee@gmail.com',
    #         'username': 'abcteddfmpusesr'
    #     }
    #     create_teacher(payload['email'], payload['username'])
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': payload['email']
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_add_admin_success_by_other_active_admin(self):
    #     """Test that other active admin can add another admin"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #
    #     # Adding current user as admin
    #     new_admin_perm = models.InstituteAdmin.objects.create(
    #         institute=institute,
    #         inviter=owner,
    #         invitee=self.user
    #     )
    #     new_admin_perm.active = True
    #     new_admin_perm.save()
    #     new_admin_perm.refresh_from_db()
    #
    #     # Creating new user
    #     payload = {
    #         'email': 'abasdfsfc@gmail.com',
    #         'username': 'abcsdfastempuser'
    #     }
    #     create_teacher(
    #         email=payload['email'],
    #         username=payload['username']
    #     )
    #
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': payload['email']
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['requested'], 'True')
    #
    # def test_duplicate_add_admin_fails(self):
    #     """Test that admin can not be added two times for same user"""
    #     institute = create_institute(self.user)
    #     payload = {
    #         'email': 'abc@gmail.com',
    #         'username': 'abctempuser'
    #     }
    #     create_teacher(
    #         email=payload['email'],
    #         username=payload['username']
    #     )
    #     self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': payload['email'],
    #             'institute_slug': institute.institute_slug
    #         })
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': payload['email']
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data['error'], 'Invitation already sent.')
    #
    # def test_can_not_invite_active_faculty_as_admin(self):
    #     """Test that faculty can not be invited as admin"""
    #     institute = create_institute(self.user)
    #     faculty = create_teacher()
    #     faculty_perm = models.InstituteFaculty.objects.create(
    #         institute=institute,
    #         inviter=self.user,
    #         invitee=faculty
    #     )
    #     faculty_perm.active = True
    #     faculty_perm.save()
    #
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': str(faculty)
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data['error'], 'Revoke faculty permission and try again.')
    #
    # def test_can_not_invite_inactive_faculty_as_admin(self):
    #     """Test that inactive faculty can not be invited as admin"""
    #     institute = create_institute(self.user)
    #     faculty = create_teacher()
    #     models.InstituteFaculty.objects.create(
    #         institute=institute,
    #         inviter=self.user,
    #         invitee=faculty
    #     )
    #
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': str(faculty)
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data['error'], 'Delete faculty invitation and try again.')
    #
    # def test_can_not_invite_active_staff_as_admin(self):
    #     """Test that staff can not be invited as admin"""
    #     institute = create_institute(self.user)
    #     staff = create_teacher()
    #     staff_perm = models.InstituteStaff.objects.create(
    #         institute=institute,
    #         inviter=self.user,
    #         invitee=staff
    #     )
    #     staff_perm.active = True
    #     staff_perm.save()
    #
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': str(staff)
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data['error'], 'Revoke staff permission and try again.')
    #
    # def test_can_not_invite_inactive_staff_as_admin(self):
    #     """Test that inactive staff can not be invited as admin"""
    #     institute = create_institute(self.user)
    #     staff = create_teacher()
    #     models.InstituteStaff.objects.create(
    #         institute=institute,
    #         inviter=self.user,
    #         invitee=staff
    #     )
    #
    #     res = self.client.post(
    #         get_admin_add_url(institute.institute_slug), {
    #             'invitee': str(staff)
    #         })
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         res.data['error'], 'Delete staff invitation and try again.')

#     def test_requested_teacher_can_accept_admin_request(self):
#         """Test that requested user can accept join request"""
#         new_user = create_teacher()
#         institute = create_institute(new_user)
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=new_user,
#             invitee=self.user
#         )
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'})
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#
#     def test_other_teacher_can_not_accept_admin_request(self):
#         """Test that other teacher can not accept join request"""
#         new_user = create_teacher()
#         invitee = create_teacher('absqwert@gmail.com', 'malinga')
#         institute = create_institute(new_user)
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=new_user,
#             invitee=invitee
#         )
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             res.data['error'],
#             'Invitation may have been deleted or you are unauthorized to perform this action.')
#
#     def test_duplicate_admin_accept_by_teacher_fails(self):
#         """Test that invitee can not accept request two times"""
#         invitee = create_teacher('absqwert@gmail.com', 'malinga')
#         institute = create_institute(self.user)
#         admin_request = models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=invitee
#         )
#         admin_request.active = True
#         admin_request.save()
#
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             res.data['error'],
#             'Invitation already accepted.')
#
#     def test_invitee_decline_admin_request_success(self):
#         """Test that invitee can decline admin join request"""
#         new_user = create_teacher()
#         institute = create_institute(new_user)
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=new_user,
#             invitee=self.user
#         )
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'})
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteAdmin.objects.filter(
#             institute=institute,
#             inviter=new_user,
#             invitee=self.user
#         ).exists())
#
#     def test_invitee_decline_admin_request_twice_fails(self):
#         """Test that invitee can not decline admin join request twice"""
#         new_user = create_teacher()
#         institute = create_institute(new_user)
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=new_user,
#             invitee=self.user
#         )
#         models.InstituteAdmin.objects.filter(
#             institute=institute,
#             inviter=new_user,
#             invitee=self.user
#         ).delete()
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             res.data['error'], 'Invitation may have been deleted already.')
#
#     def test_inviter_can_cancel_admin_join_request(self):
#         """Test that inviter can cancel invitee join request"""
#         new_user = create_teacher()
#         institute = create_institute(self.user)
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=new_user
#         )
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)})
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteAdmin.objects.filter(
#             institute=institute,
#             inviter=self.user,
#             invitee=new_user
#         ).exists())
#
#     def test_active_admin_can_cancel_admin_join_request(self):
#         """Test that active admin can cancel invitee join request"""
#         new_user = create_teacher()
#         institute = create_institute(self.user, 'Focus institute')
#
#         # Activating another admin and initiating request
#         active_admin = create_teacher('active@gmail.com', 'activeadmin')
#         request = models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=active_admin
#         )
#         request.active = True
#         request.save()
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=active_admin,
#             invitee=new_user
#         )
#
#         # Authenticated another admin deleting request
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)})
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteAdmin.objects.filter(
#             institute=institute,
#             inviter=active_admin,
#             invitee=new_user
#         ).exists())
#
#     def test_non_admin_can_not_delete_admin_join_request(self):
#         """Test that non admin can not delete admin join request"""
#         new_user = create_teacher()
#         institute = create_institute(new_user)
#         invitee = create_teacher('invitee@gmail.com', 'invitee')
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             invitee=invitee,
#             inviter=new_user
#         )
#
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(new_user)})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             res.data['error'],
#             'You don\'t have permission to delete the request.')
#
#     def test_institute_owner_can_not_delete_admin_role_of_self(self):
#         """Test institute owner delete self owner role fails"""
#         institute = create_institute(self.user)
#         res = self.client.post(
#             get_admin_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'})
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             res.data['error'],
#             'Owner can\'t remove self admin role without appointing another owner.')
#
#     def test_staff_can_accept_staff_role_request(self):
#         """Test that staff can accept institution staff join request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         add_staff_role(owner, self.user, institute)
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#         self.assertTrue(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=self.user,
#             active=True
#         ).exists())
#
#     def test_staff_can_not_re_accept_staff_role_request(self):
#         """Test that staff can re-accept institution staff join request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         role = add_staff_role(owner, self.user, institute)
#         role.active = True
#         role.save()
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Staff role request already accepted.')
#         self.assertTrue(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=self.user,
#             active=True
#         ).exists())
#
#     def test_inviter_can_not_pre_accept_staff_role_request(self):
#         """Test that inviter can not activate staff role while inviting"""
#         new_staff = create_teacher()
#         institute = create_institute(self.user)
#         with self.assertRaises(Exception):
#             add_staff_role(self.user, new_staff, institute, True)
#
#     def test_invitee_can_decline_staff_role_request(self):
#         """Test that invitee can decline staff role request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         add_staff_role(owner, self.user, institute)
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=self.user
#         ).exists())
#
#     def test_active_admin_can_decline_staff_role_request(self):
#         """Test active admin users can delete staff role request"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         add_staff_role(self.user, staff, institute)
#
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=staff
#         ).exists())
#
#     def test_any_active_admin_can_decline_staff_role_request(self):
#         """Test any active admin users can delete staff role request"""
#         owner = create_teacher('owneraa@gmail.com', 'owneraa')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         role = models.InstituteAdmin.objects.create(
#             inviter=owner,
#             invitee=self.user,
#             institute=institute
#         )
#         role.active = True
#         role.save()
#         add_staff_role(owner, staff, institute)
#
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=staff
#         ).exists())
#
#     def test_inactive_admin_cannot_decline_staff_role_request(self):
#         """Test inactive admin users can not delete staff role request"""
#         owner = create_teacher('owneruser@gmail.com', 'jkarta')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         add_staff_role(owner, staff, institute)
#         models.InstituteStaff.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user
#         )
#
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertTrue(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=staff
#         ).exists())
#
#     def test_non_admin_cannot_decline_staff_role_request(self):
#         """Test non admin users can not delete staff role request"""
#         owner = create_teacher('owneruser@gmail.com', 'jkarta')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         add_staff_role(owner, staff, institute)
#
#         res = self.client.post(
#             get_staff_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(staff)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertTrue(models.InstituteStaff.objects.filter(
#             institute=institute,
#             invitee=staff
#         ).exists())
#
#     def test_invitee_can_accept_faculty_request(self):
#         """Test that faculty can accept faculty join request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         add_faculty_role(owner, self.user, institute)
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'ACCEPTED')
#         self.assertTrue(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=self.user,
#             active=True
#         ).exists())
#
#     def test_inviter_cannot_pre_activate_faculty_request(self):
#         """Test that inviter can not pre-activate faculty role"""
#         institute = create_institute(self.user)
#         new_user = create_teacher()
#         with self.assertRaises(Exception):
#             add_faculty_role(self.user, new_user, institute, True)
#
#     def test_non_invitee_can_not_accept_faculty_join_request(self):
#         """Test that non invitee can not accept request"""
#         owner = create_teacher()
#         invitee = create_teacher('invittee@gmail.com', 'invitee')
#         institute = create_institute(owner)
#         add_faculty_role(owner, invitee, institute)
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'ACCEPT'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Invitation deleted or insufficient permission to accept.')
#
#     def test_invitee_can_delete_faculty_join_request(self):
#         """Test that invitee can delete join request"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         add_faculty_role(owner, self.user, institute)
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE'}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=self.user
#         ).exists())
#
#     def test_active_admin_can_delete_faculty_join_request(self):
#         """Test that active admin can delete faculty"""
#         faculty = create_teacher()
#         institute = create_institute(self.user)
#         add_faculty_role(self.user, faculty, institute)
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=faculty
#         ).exists())
#
#     def test_any_active_admin_can_delete_faculty_join_request(self):
#         """Test that any active admin can delete faculty"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         faculty = create_teacher('facultdy@gmail.com', 'facultydf')
#         add_faculty_role(owner, faculty, institute)
#
#         role = models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user
#         )
#         role.active = True
#         role.save()
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['status'], 'DELETED')
#         self.assertFalse(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=faculty
#         ).exists())
#
#     def test_inactive_admin_can_not_delete_faculty_join_request(self):
#         """Test that inactive admin can not delete faculty"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         faculty = create_teacher('facultdy@gmail.com', 'facultydf')
#         add_faculty_role(owner, faculty, institute)
#
#         models.InstituteAdmin.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user
#         )
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertTrue(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=faculty
#         ).exists())
#
#     def test_anyone_can_not_delete_faculty_join_request(self):
#         """Test that anyone can not delete faculty"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         faculty = create_teacher('facultdy@gmail.com', 'facultydf')
#         add_faculty_role(owner, faculty, institute)
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertTrue(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=faculty
#         ).exists())
#
#     def test_staff_can_not_delete_faculty_join_request(self):
#         """Test that staff can not delete faculty"""
#         owner = create_teacher()
#         institute = create_institute(owner)
#         faculty = create_teacher('facultdy@gmail.com', 'facultydf')
#         add_faculty_role(owner, faculty, institute)
#
#         role = models.InstituteStaff.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user
#         )
#         role.active = True
#         role.save()
#
#         res = self.client.post(
#             get_faculty_accept_delete_url(institute.institute_slug),
#             {'operation': 'DELETE', 'invitee': str(faculty)}
#         )
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'], 'Insufficient permission.')
#         self.assertTrue(models.InstituteFaculty.objects.filter(
#             institute=institute,
#             invitee=faculty
#         ).exists())
#
#
    def test_add_staff_success_by_owner(self):
        """Test that staff add is success by admin owner"""
        institute = create_institute(self.user)
        staff = create_teacher()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(staff)}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'INVITED')
        self.assertTrue(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=staff
        ).exists())

    def test_add_staff_success_by_any_active_admin(self):
        """Test that staff add success by any admin"""
        owner = create_teacher()
        institute = create_institute(owner)
        staff = create_teacher('staffqw@gmail.com', 'staffuser')
        role = models.InstituteAdmin.objects.create(
            institute=institute,
            invitee=self.user,
            inviter=owner
        )
        role.active = True
        role.save()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(staff)}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'INVITED')
        self.assertTrue(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=staff
        ).exists())

    def test_add_staff_fails_for_inactive_admin(self):
        """Test that staff add failure by inactive admin"""
        owner = create_teacher()
        institute = create_institute(owner)
        staff = create_teacher('staffqw@gmail.com', 'staffuser')
        models.InstituteAdmin.objects.create(
            institute=institute,
            invitee=self.user,
            inviter=owner
        )

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(staff)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Insufficient permission.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=staff
        ).exists())

    def test_add_staff_fails_for_other_users(self):
        """Test that staff add failure by other users"""
        owner = create_teacher()
        institute = create_institute(owner)
        staff = create_teacher('staffqw@gmail.com', 'staffuser')
        role = models.InstituteStaff.objects.create(
            institute=institute,
            invitee=self.user,
            inviter=owner
        )
        role.active = True
        role.save()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(staff)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Insufficient permission.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=staff
        ).exists())

    def test_add_wrong_email_staff_fails_by_owner(self):
        """Test that staff add fails if email is wrong by admin owner"""
        institute = create_institute(self.user)
        staff = create_teacher()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': 'bla@gmail.com'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'This user does not exist. Correct the email and try again.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=staff
        ).exists())

    def test_can_not_invite_self_as_staff(self):
        """Test that can not invite self as staff"""
        institute = create_institute(self.user)
        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(self.user)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'User already has admin permissions.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    def test_can_not_invite_other_active_admin_as_staff(self):
        """Test that can not invite other active admin as staff"""
        institute = create_institute(self.user)
        admin = create_teacher()
        role = models.InstituteAdmin.objects.create(
            institute=institute,
            inviter=self.user,
            invitee=admin
        )
        role.active = True
        role.save()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(admin)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'User already has admin permissions.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    def test_can_not_invite_other_inactive_admin_as_staff(self):
        """Test that can not invite other inactive admin as staff"""
        institute = create_institute(self.user)
        admin = create_teacher()
        models.InstituteAdmin.objects.create(
            institute=institute,
            inviter=self.user,
            invitee=admin
        )

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(admin)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Revoke user admin invitation and try again.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    def test_can_not_invite_other_inactive_faculty_as_staff(self):
        """Test that can not invite other inactive faculty as staff"""
        institute = create_institute(self.user)
        admin = create_teacher()
        models.InstituteFaculty.objects.create(
            institute=institute,
            inviter=self.user,
            invitee=admin
        )

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(admin)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Remove faculty invitation and try again.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    def test_can_not_invite_other_active_faculty_as_staff(self):
        """Test that can not invite other inactive faculty as staff"""
        institute = create_institute(self.user)
        admin = create_teacher()
        role = models.InstituteFaculty.objects.create(
            institute=institute,
            inviter=self.user,
            invitee=admin
        )
        role.active = True
        role.save()

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(admin)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Remove faculty permission and try again.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    def test_can_not_re_invite_for_staff(self):
        """Test that can not re-invite staff as staff"""
        institute = create_institute(self.user)
        staff = create_teacher()
        models.InstituteFaculty.objects.create(
            institute=institute,
            inviter=self.user,
            invitee=staff
        )

        res = self.client.post(
            get_staff_add_url(institute.institute_slug),
            {'invitee': str(staff)}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'User already invited.')
        self.assertFalse(models.InstituteStaff.objects.filter(
            institute=institute,
            invitee=self.user
        ).exists())

    # def test_add_faculty_success_by_owner(self):
    #     """Test that faculty add is success by admin owner"""
    #     institute = create_institute(self.user)
    #     faculty = create_teacher()
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'INVITED')
    #     self.assertTrue(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_faculty_success_by_any_active_admin(self):
    #     """Test that faculty add success by any admin"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #     faculty = create_teacher('facultyw@gmail.com', 'facultyuser')
    #     role = models.InstituteAdmin.objects.create(
    #         institute=institute,
    #         invitee=self.user,
    #         inviter=owner
    #     )
    #     role.active = True
    #     role.save()
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'INVITED')
    #     self.assertTrue(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_faculty_fails_for_inactive_admin(self):
    #     """Test that faculty add failure by inactive admin"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #     faculty = create_teacher('facultysdf@gmail.com', 'faculty')
    #     models.InstituteAdmin.objects.create(
    #         institute=institute,
    #         invitee=self.user,
    #         inviter=owner
    #     )
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Insufficient permission.')
    #     self.assertFalse(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_faculty_success_for_active_staff(self):
    #     """Test that faculty add success by active staff"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #     faculty = create_teacher('faculty@gmail.com', 'faculty')
    #     role = models.InstituteStaff.objects.create(
    #         institute=institute,
    #         invitee=self.user,
    #         inviter=owner
    #     )
    #     role.active = True
    #     role.save()
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'INVITED')
    #     self.assertTrue(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_faculty_fails_for_inactive_staff(self):
    #     """Test that faculty add failure by inactive staff"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #     faculty = create_teacher('faculty@gmail.com', 'faculty')
    #     models.InstituteStaff.objects.create(
    #         institute=institute,
    #         invitee=self.user,
    #         inviter=owner
    #     )
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Insufficient permission.')
    #     self.assertFalse(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_faculty_fails_for_other_users(self):
    #     """Test that faculty add failure by other users"""
    #     owner = create_teacher()
    #     institute = create_institute(owner)
    #     faculty = create_teacher('facultyqw@gmail.com', 'faculty')
    #     role = models.InstituteStaff.objects.create(
    #         institute=institute,
    #         invitee=self.user,
    #         inviter=owner
    #     )
    #     role.active = True
    #     role.save()
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(faculty)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Insufficient permission.')
    #     self.assertFalse(models.InstituteStaff.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_add_wrong_email_faculty_fails_by_owner(self):
    #     """Test that staff add fails if email is wrong by admin owner"""
    #     institute = create_institute(self.user)
    #     faculty = create_teacher()
    #
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': 'bla@gmail.com'}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This user does not exist. Correct the email and try again.')
    #     self.assertFalse(models.InstituteStaff.objects.filter(
    #         institute=institute,
    #         invitee=faculty
    #     ).exists())
    #
    # def test_can_not_invite_self_as_faculty(self):
    #     """Test that can not invite self as faculty"""
    #     institute = create_institute(self.user)
    #     res = self.client.post(
    #         get_faculty_add_url(institute.institute_slug),
    #         {'invitee': str(self.user)}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Can not invite self as faculty.')
    #     self.assertFalse(models.InstituteFaculty.objects.filter(
    #         institute=institute,
    #         invitee=self.user
    #     ).exists())


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
#     def test_get_not_allowed_on_institute_admin_add_url(self):
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
#         res = self.client.get(get_admin_add_url(institute.institute_slug))
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
#             get_admin_add_url(institute_slug), {
#                 'email': payload['email'],
#                 'institute_slug': institute_slug
#             })
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


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
#     def test_get_not_allowed_on_institute_admin_add_url(self):
#         """Test that get is not allowed by user on institute admin add url"""
#         teacher_user = create_teacher()
#         institute = models.Institute.objects.create(
#             user=teacher_user,
#             name='Whatever whatever',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#         res = self.client.get(get_admin_add_url(institute.institute_slug))
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
#             get_admin_add_url(institute_slug), {
#                 'email': payload['email'],
#                 'institute_slug': institute_slug
#             })
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
