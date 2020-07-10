# import os
# import datetime
#
# from unittest.mock import patch
#
# from django.db import IntegrityError
# from django.test import TestCase
# from django.contrib.auth import get_user_model
#
# from core import models
# from django.core.exceptions import PermissionDenied
# from django.utils import timezone
#
#
# def create_teacher(email='teacher@gmail.com', username='tempusername'):
#     """Creates and return teacher user"""
#     return get_user_model().objects.create_user(
#         email=email,
#         password='teacherpassword',
#         username=username,
#         is_teacher=True
#     )
#
#
# def create_student(email='student@gmail.com', username='tempsdffd'):
#     """Creates and return student user"""
#     return get_user_model().objects.create_user(
#         email=email,
#         password='teacherpassword',
#         username=username,
#         is_student=True
#     )
#
#
# def create_user(email='user@gmail.com', username='usertemp'):
#     """Creates and return student user"""
#     return get_user_model().objects.create_user(
#         email=email,
#         password='teacherpassword',
#         username=username
#     )
#
#
# # class InstituteModelTests(TestCase):
# #     """Test the institute model"""
# #
# #     def test_teacher_create_institute_success(self):
# #         """
# #         Test that creation of institute is
# #         successful for teacher with minimal details.
# #         """
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         res = models.Institute.objects.create(**payload)
# #
# #         self.assertTrue(models.Institute.objects.filter(
# #             name=payload['name'].lower()).exists())
# #         self.assertEqual(res.user, user)
# #         self.assertEqual(res.name, payload['name'].lower())
# #         self.assertEqual(res.institute_category, payload['institute_category'])
# #         self.assertEqual(res.country, 'IN')
# #         self.assertEqual(res.institute_profile.motto, '')
# #
# #     def test_duplicate_institute_fails(self):
# #         """
# #         Test that creation of duplicate institute
# #         fails for teacher.
# #         """
# #         payload = {
# #             'user': create_teacher(),
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         models.Institute.objects.create(**payload)
# #
# #         with self.assertRaises(IntegrityError):
# #             models.Institute.objects.create(**payload)
# #
# #     def test_user_institute_name_unique_together_success(self):
# #         """
# #         Test that creation of institute succeeds
# #         for different teacher but with same institute name.
# #         """
# #         payload = {
# #             'user': create_teacher(),
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         payload1 = {
# #             'user': create_teacher('temp@gmail.com', 'newusername'),
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         models.Institute.objects.create(**payload)
# #         models.Institute.objects.create(**payload1)
# #
# #         self.assertEqual(len(models.Institute.objects.filter(
# #             name=payload['name'].lower()
# #         )), 2)
# #
# #     def test_teacher_create_invalid_institute_fails(self):
# #         """
# #         Test that creation of institute
# #         fails for teacher with invalid details.
# #         """
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': '   ',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #
# #         with self.assertRaises(ValueError):
# #             models.Institute.objects.create(**payload)
# #
# #     def test_student_create_institute_fails(self):
# #         """
# #         Test that creation of institute
# #         fails for student.
# #         """
# #         user = create_student()
# #         payload = {
# #             'user': user,
# #             'name': 'My Educational Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #
# #         with self.assertRaises(PermissionDenied):
# #             models.Institute.objects.create(**payload)
# #
# #     def test_institute_slug(self):
# #         """
# #         Test that creation of institute is
# #         successful for teacher with minimal details.
# #         """
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         res = models.Institute.objects.create(**payload)
# #
# #         self.assertTrue(models.Institute.objects.filter(
# #             name=payload['name'].lower()).exists())
# #
# #         starts_with = res.institute_slug.startswith('my-custom-institute')
# #         self.assertTrue(starts_with)
# #
# #     def test_string_representation_institute_model(self):
# #         """Test string representation of institute model"""
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         res = models.Institute.objects.create(**payload)
# #         self.assertEqual(str(res), payload['name'].lower())
# #
# #     def test_admin_is_created_for_institute_automatically(self):
# #         """
# #         Test that owner is set as admin automatically
# #         """
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         institute = models.Institute.objects.create(**payload)
# #         self.assertTrue(models.InstituteAdmin.objects.filter(
# #             institute=institute,
# #             invitee=user,
# #             active=True
# #         ).exists())
#
#
#
# # class InstituteProfileModelTests(TestCase):
# #     """Tests for institute profile model."""
# #
# #     def test_teacher_create_institute_profile_full_details(self):
# #         """
# #         Test that creation of institute profile is
# #         successful for teacher with full details.
# #         """
# #         payload = {
# #             'user': create_teacher(),
# #             'name': 'My Custom Institute12',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #             'institute_profile': {
# #                 'motto': 'This is custom moto.',
# #                 'email': 'xyz@gmail.com',
# #                 'phone': '+918787878787',
# #                 'website_url': 'https://www.google.com',
# #                 'state': 'TR',
# #                 'address': 'xyz road',
# #                 'pin': '799250',
# #                 'recognition': 'ICSE'
# #             }
# #         }
# #         institute_profile = payload['institute_profile']
# #         res = models.Institute.objects.create(
# #             user=payload['user'],
# #             name=payload['name'],
# #             institute_category=payload['institute_category'],
# #         )
# #
# #         res.institute_profile.motto = institute_profile['motto']
# #         res.institute_profile.email = institute_profile['email']
# #         res.institute_profile.phone = institute_profile['phone']
# #         res.institute_profile.website_url = institute_profile['website_url']
# #         res.institute_profile.state = institute_profile['state']
# #         res.institute_profile.address = institute_profile['address']
# #         res.institute_profile.pin = institute_profile['pin']
# #         res.institute_profile.recognition = institute_profile['recognition']
# #         res.save()
# #
# #         res1 = models.InstituteProfile.objects.get(institute=res)
# #
# #         self.assertTrue(models.Institute.objects.filter(
# #             name=payload['name'].lower()).exists())
# #         self.assertEqual(res1.motto, institute_profile['motto'])
# #         self.assertEqual(res1.email, institute_profile['email'])
# #         self.assertEqual(res1.phone, institute_profile['phone'])
# #         self.assertEqual(res1.website_url, institute_profile['website_url'])
# #         self.assertEqual(res1.state, institute_profile['state'])
# #         self.assertEqual(res1.address, institute_profile['address'])
# #         self.assertEqual(res1.pin, institute_profile['pin'])
# #         self.assertEqual(res1.recognition, institute_profile['recognition'])
# #
# #     def test_institute_profile_string_representation(self):
# #         """Test that institute profile is correctly represented"""
# #         user = create_teacher()
# #         payload = {
# #             'user': user,
# #             'name': 'My Custom Institute',
# #             'institute_category': models.InstituteCategory.EDUCATION,
# #         }
# #         institute = models.Institute.objects.create(**payload)
# #         institute_profile = models.InstituteProfile.objects.get(
# #             institute=institute)
# #         self.assertEqual(str(institute_profile), str(institute))
# #
# #     @patch('uuid.uuid4')
# #     def test_institute_image_upload_url_uuid(self, mock_url):
# #         """Test that institute image is uploaded in correct location"""
# #         uuid = 'test-uuid'
# #         mock_url.return_value = uuid
# #         file_path = models.institute_logo_upload_file_path(
# #             None, 'img.jpg')
# #         dt = datetime.date.today()
# #         path = 'pictures/uploads/institute/logo'
# #         ini_path = f'{path}/{dt.year}/{dt.month}/{dt.day}'
# #         expected_path = os.path.join(ini_path, f'{uuid}.jpg')
# #         self.assertEqual(file_path, expected_path)
# #
# #     @patch('uuid.uuid4')
# #     def test_institute_banner_upload_url_uuid(self, mock_url):
# #         """Test that institute banner is uploaded in correct location"""
# #         uuid = 'test-uuid'
# #         mock_url.return_value = uuid
# #         file_path = models.institute_banner_upload_file_path(
# #             None, 'img.png'
# #         )
# #         dt = datetime.date.today()
# #         path = 'pictures/uploads/institute/banner'
# #         ini_path = f'{path}/{dt.year}/{dt.month}/{dt.day}'
# #         expected_path = os.path.join(ini_path, f'{uuid}.png')
# #         self.assertEqual(file_path, expected_path)
#
#
# # class InstituteAdminModelTests(TestCase):
# #     """Tests for institute admin model"""
# #
# #     def setUp(self):
# #         self.user = create_user()
# #         self.teacher = create_teacher()
# #         self.teacher1 = create_teacher('teacher1@gmail.com', 'staff')
# #         self.student = create_student()
# #
# #         self.institute = models.Institute.objects.create(
# #             user=self.teacher,
# #             name='Holy Crap',
# #             institute_category=models.InstituteCategory.EDUCATION
# #         )
# #
# #     def test_owner_is_set_as_admin_automatically(self):
# #         """Test that owner of institute is set as admin automatically"""
# #         self.assertTrue(models.InstituteAdmin.objects.filter(
# #             inviter=self.teacher,
# #             invitee=self.teacher,
# #             active=True,
# #             institute=self.institute
# #         ).exists())
# #
# #     def test_admin_invite_others_success(self):
# #         """
# #         Test that admin can invite other teacher for admin
# #         """
# #         permission = models.InstituteAdmin.objects.create(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=self.teacher1,
# #         )
# #
# #         self.assertEqual(permission.active, False)
# #         self.assertEqual(permission.inviter, self.teacher)
# #         self.assertEqual(permission.invitee, self.teacher1)
# #
# #     def test_pre_activate_permission_for_other_admin_fails(self):
# #         """
# #         Test that inviter can not accept the join request for
# #         other admin user of same institute
# #         """
# #         with self.assertRaises(PermissionDenied):
# #             models.InstituteAdmin.objects.create(
# #                 institute=self.institute,
# #                 inviter=self.teacher,
# #                 invitee=self.teacher1,
# #                 active=True
# #             )
# #
# #     def test_can_not_invite_if_not_owner(self):
# #         """
# #         Test that inviter can not invite himself
# #         if he is not owner of institute
# #         """
# #         with self.assertRaises(PermissionDenied):
# #             models.InstituteAdmin.objects.create(
# #                 institute=self.institute,
# #                 inviter=self.teacher1,
# #                 invitee=self.teacher1,
# #                 active=True
# #             )
# #
# #     def test_can_only_appoint_teacher_user_as_admin(self):
# #         """Test that inviter can not invite other user as admin"""
# #         with self.assertRaises(PermissionDenied):
# #             models.InstituteAdmin.objects.create(
# #                 institute=self.institute,
# #                 inviter=self.teacher,
# #                 invitee=self.student
# #             )
# #
# #     def test_invitation_of_admin_by_others_fails(self):
# #         """Test that invitation of admin by other user fails"""
# #         new_teacher = create_teacher('teacddfdf@gmail.com', 'honkings')
# #         with self.assertRaises(PermissionDenied):
# #             models.InstituteAdmin.objects.create(
# #                 institute=self.institute,
# #                 inviter=self.teacher1,
# #                 invitee=new_teacher,
# #                 active=True
# #             )
# #
# #     def test_accept_invitation_by_admin_success(self):
# #         """Test that accepting invitation by admin success"""
# #         admin_perm = models.InstituteAdmin.objects.create(
# #                     institute=self.institute,
# #                     inviter=self.teacher,
# #                     invitee=self.teacher1,
# #                 )
# #         admin_perm.active = True
# #         accepting_time = timezone.now()
# #         admin_perm.request_accepted_on = accepting_time
# #         admin_perm.save()
# #         admin_perm.refresh_from_db()
# #
# #         self.assertTrue(admin_perm.active)
# #         self.assertEqual(
# #             admin_perm.request_accepted_on, accepting_time)
# #
# #     def test_string_representation_admin_permission_model(self):
# #         """Test the string representation of admin permission model"""
# #         permission = models.InstituteAdmin.objects.create(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=self.teacher1,
# #         )
# #
# #         self.assertEqual(str(permission), str(self.teacher1))
# #
# #     def test_delete_admin_request_success(self):
# #         """Test that admin delete request is success"""
# #         permission = models.InstituteAdmin.objects.create(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=self.teacher1,
# #         )
# #         models.InstituteAdmin.objects.filter(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=self.teacher1,
# #         ).delete()
# #         self.assertFalse(models.InstituteAdmin.objects.filter(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=self.teacher1,
# #         ).exists())
# #
# #     def test_add_admin_by_non_owner_active_admin_success(self):
# #         """Test that adding admin by non owner active admin success"""
# #         # Creating an additional admin
# #         new_active_admin = create_teacher('abdddd@gmail.com', 'abyassssf')
# #         admin_perm = models.InstituteAdmin.objects.create(
# #             institute=self.institute,
# #             inviter=self.teacher,
# #             invitee=new_active_admin
# #         )
# #         admin_perm.active = True
# #         admin_perm.save()
# #
# #         models.InstituteAdmin.objects.create(
# #             institute=self.institute,
# #             inviter=new_active_admin,
# #             invitee=self.teacher1
# #         )
# #         self.assertTrue(models.InstituteAdmin.objects.filter(
# #             institute=self.institute,
# #             inviter=new_active_admin,
# #             invitee=self.teacher1
# #         ).exists())
#
#
# class InstituteStaffModelTests(TestCase):
#     """Tests for institute staff model"""
#
#     def setUp(self):
#         self.user = create_user()
#         self.teacher = create_teacher()
#         self.teacher1_active = create_teacher(
#             'teacher1@gmail.com', 'teacher1')
#         self.teacher2_inactive = create_teacher(
#             'teacher2@gmail.com', 'teacher2')
#         self.staff = create_teacher('staff@gmail.com', 'staff')
#         self.faculty = create_teacher('faculty@gmail.com', 'faculty')
#         self.student = create_student()
#
#         self.institute = models.Institute.objects.create(
#             user=self.teacher,
#             name='Holy Crap',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#
#         models.InstituteAdmin.objects.create(
#             institute=self.institute,
#             inviter=self.teacher,
#             invitee=self.teacher2_inactive,
#         )
#
#         admin_perm = models.InstituteAdmin.objects.create(
#             institute=self.institute,
#             inviter=self.teacher,
#             invitee=self.teacher1_active,
#         )
#         admin_perm.active = True
#         admin_perm.save()
#
#     def test_add_staff_user_by_owner_success(self):
#         """Test that adding staff to institute by owner success"""
#         permission = models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.teacher,
#             invitee=self.staff,
#         )
#
#         self.assertEqual(permission.active, False)
#         self.assertEqual(permission.institute, self.institute)
#         self.assertEqual(permission.inviter, self.teacher)
#         self.assertEqual(permission.invitee, self.staff)
#
#     def test_add_staff_user_by_other_active_admin_success(self):
#         """Test that adding staff to institute by active admin success"""
#         permission = models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.teacher1_active,
#             invitee=self.staff,
#         )
#
#         self.assertEqual(permission.active, False)
#         self.assertEqual(permission.institute, self.institute)
#         self.assertEqual(permission.inviter, self.teacher1_active)
#         self.assertEqual(permission.invitee, self.staff)
#
#     def test_add_staff_user_by_other_inactive_admin_failure(self):
#         """Test that adding staff to institute by admin success"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteStaff.objects.create(
#                 institute=self.institute,
#                 inviter=self.teacher2_inactive,
#                 invitee=self.staff,
#             )
#
#     def test_pre_activate_permission_fails(self):
#         """Test that inviter can not accept the join request"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteStaff.objects.create(
#                 institute=self.institute,
#                 inviter=self.teacher,
#                 invitee=self.staff,
#                 active=True
#             )
#
#     def test_cannot_invite_self(self):
#         """Test that inviter can not invite himself"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteStaff.objects.create(
#                 institute=self.institute,
#                 inviter=self.teacher,
#                 invitee=self.teacher,
#                 active=True
#             )
#
#     def test_can_only_appoint_teacher_user_as_staff(self):
#         """Test that inviter can not invite student user as staff"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteStaff.objects.create(
#                 institute=self.institute,
#                 inviter=self.teacher,
#                 invitee=self.student
#             )
#
#     def test_invitation_of_staff_by_others_fails(self):
#         """Test that invitation of staff by other user fails"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteStaff.objects.create(
#                 institute=self.institute,
#                 inviter=self.faculty,
#                 invitee=self.staff
#             )
#
#     def test_accept_staff_invitation_success(self):
#         """Test that accepting invitation by staff success"""
#         staff_perm = models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.teacher,
#             invitee=self.staff,
#         )
#         staff_perm.active = True
#         staff_perm.save()
#         staff_perm.refresh_from_db()
#
#         self.assertTrue(staff_perm.active)
#
#     def test_string_representation_staff_permission_model(self):
#         """Test the string representation of staff permission model"""
#         permission = models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.teacher,
#             invitee=self.staff,
#         )
#
#         self.assertEqual(str(permission), str(self.staff))
#
#
# class InstituteFacultyModelTests(TestCase):
#     """Tests for institute faculty model"""
#
#     def setUp(self):
#         self.user = create_user()
#         self.owner = create_teacher()
#         self.admin_active = create_teacher(
#             'teacher1@gmail.com', 'teacher1')
#         self.admin_inactive = create_teacher(
#             'teacher2@gmail.com', 'teacher2')
#         self.faculty = create_teacher('faculty@gmail.com', 'faculty')
#         self.teacher = create_teacher('teachos@gmail.com', 'tachos')
#         self.staff_active = create_teacher('staff@gmail.com', 'stafff')
#         self.staff_inactive = create_teacher('instaff@gmail.com', 'sintafff')
#         self.student = create_student()
#
#         self.institute = models.Institute.objects.create(
#             user=self.owner,
#             name='Holy Crap',
#             institute_category=models.InstituteCategory.EDUCATION
#         )
#
#         models.InstituteAdmin.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.admin_inactive,
#         )
#
#         admin_perm = models.InstituteAdmin.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.admin_active,
#         )
#         admin_perm.active = True
#         admin_perm.save()
#
#         models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.staff_inactive,
#         )
#
#         admin_perm = models.InstituteStaff.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.staff_active,
#         )
#         admin_perm.active = True
#         admin_perm.save()
#
#     def test_add_faculty_user_by_owner_success(self):
#         """Test that adding faculty to institute by owner success"""
#         permission = models.InstituteFaculty.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.faculty,
#         )
#
#         self.assertEqual(permission.active, False)
#         self.assertEqual(permission.institute, self.institute)
#         self.assertEqual(permission.inviter, self.owner)
#         self.assertEqual(permission.invitee, self.faculty)
#
#     def test_add_faculty_user_by_other_active_admin_success(self):
#         """Test that adding faculty to institute by active admin success"""
#         permission = models.InstituteFaculty.objects.create(
#             institute=self.institute,
#             inviter=self.admin_active,
#             invitee=self.faculty,
#         )
#
#         self.assertEqual(permission.active, False)
#         self.assertEqual(permission.institute, self.institute)
#         self.assertEqual(permission.inviter, self.admin_active)
#         self.assertEqual(permission.invitee, self.faculty)
#
#     def test_add_faculty_user_by_other_active_staff_success(self):
#         """Test that adding faculty to institute by active staff success"""
#         permission = models.InstituteFaculty.objects.create(
#             institute=self.institute,
#             inviter=self.staff_active,
#             invitee=self.faculty,
#         )
#
#         self.assertEqual(permission.active, False)
#         self.assertEqual(permission.institute, self.institute)
#         self.assertEqual(permission.inviter, self.staff_active)
#         self.assertEqual(permission.invitee, self.faculty)
#
#     def test_add_faculty_user_by_other_inactive_staff_fails(self):
#         """Test that adding faculty to institute by inactive staff fails"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.staff_inactive,
#                 invitee=self.faculty,
#             )
#
#     def test_add_faculty_user_by_other_inactive_admin_failure(self):
#         """Test that adding faculty to institute by inactive admin fails"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.admin_inactive,
#                 invitee=self.faculty,
#             )
#
#     def test_pre_activate_permission_fails(self):
#         """Test that inviter can not pre-activate the join request"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.owner,
#                 invitee=self.faculty,
#                 active=True
#             )
#
#     def test_cannot_invite_self_as_faculty(self):
#         """Test that inviter can not invite himself"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.admin_active,
#                 invitee=self.admin_active,
#                 active=True
#             )
#
#     def test_can_only_appoint_teacher_user_as_faculty(self):
#         """Test that inviter can not invite student user as faculty"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.owner,
#                 invitee=self.student
#             )
#
#     def test_invitation_of_faculty_by_others_fails(self):
#         """Test that invitation of faculty by other user fails"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.teacher,
#                 invitee=self.faculty
#             )
#
#     def test_invitation_of_faculty_by_normal_user_fails(self):
#         """Test that invitation of faculty by normal user fails"""
#         with self.assertRaises(PermissionDenied):
#             models.InstituteFaculty.objects.create(
#                 institute=self.institute,
#                 inviter=self.user,
#                 invitee=self.faculty
#             )
#
#     def test_accept_faculty_invitation_success(self):
#         """Test that accepting invitation by faculty success"""
#         faculty_perm = models.InstituteFaculty.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.faculty,
#         )
#         faculty_perm.active = True
#         faculty_perm.save()
#         faculty_perm.refresh_from_db()
#
#         self.assertTrue(faculty_perm.active)
#
#     def test_string_representation_faculty_permission_model(self):
#         """Test the string representation of faculty permission model"""
#         permission = models.InstituteFaculty.objects.create(
#             institute=self.institute,
#             inviter=self.owner,
#             invitee=self.faculty,
#         )
#
#         self.assertEqual(str(permission), str(self.faculty))
