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
# def create_institute(user, name='Temp Name ola'):
#     """Creates and returns an institute"""
#     return models.Institute.objects.create(
#         user=user,
#         name=name,
#         institute_category=models.InstituteCategory.EDUCATION,
#         type=models.InstituteType.COLLEGE
#     )
#
#
# class InstituteModelTests(TestCase):
#     """Test the institute model"""
#
#     def test_teacher_create_institute_success(self):
#         """
#         Test that creation of institute is
#         successful for teacher with minimal details.
#         """
#         user = create_teacher()
#         payload = {
#             'user': user,
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         res = models.Institute.objects.create(**payload)
#
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#         self.assertEqual(res.user, user)
#         self.assertEqual(res.name, payload['name'].lower())
#         self.assertEqual(res.institute_category, payload['institute_category'])
#         self.assertEqual(res.type, payload['type'])
#         self.assertEqual(res.country, 'IN')
#         self.assertEqual(res.institute_profile.motto, '')
#
#     def test_duplicate_institute_fails(self):
#         """
#         Test that creation of duplicate institute
#         fails for teacher.
#         """
#         payload = {
#             'user': create_teacher(),
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         models.Institute.objects.create(**payload)
#
#         with self.assertRaises(IntegrityError):
#             models.Institute.objects.create(**payload)
#
#     def test_user_institute_name_unique_together_success(self):
#         """
#         Test that creation of institute succeeds
#         for different teacher but with same institute name.
#         """
#         payload = {
#             'user': create_teacher(),
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         payload1 = {
#             'user': create_teacher('temp@gmail.com', 'newusername'),
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         models.Institute.objects.create(**payload)
#         models.Institute.objects.create(**payload1)
#
#         self.assertEqual(len(models.Institute.objects.filter(
#             name=payload['name'].lower()
#         )), 2)
#
#     def test_teacher_create_invalid_institute_fails(self):
#         """
#         Test that creation of institute
#         fails for teacher with invalid details.
#         """
#         user = create_teacher()
#         payload = {
#             'user': user,
#             'name': '   ',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#
#         with self.assertRaises(ValueError):
#             models.Institute.objects.create(**payload)
#
#     def test_student_create_institute_fails(self):
#         """
#         Test that creation of institute
#         fails for student.
#         """
#         user = create_student()
#         payload = {
#             'user': user,
#             'name': 'My Educational Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#
#         with self.assertRaises(PermissionDenied):
#             models.Institute.objects.create(**payload)
#
#     def test_institute_slug(self):
#         """
#         Test that creation of institute is
#         successful for teacher with minimal details.
#         """
#         user = create_teacher()
#         payload = {
#             'user': user,
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         res = models.Institute.objects.create(**payload)
#
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#
#         starts_with = res.institute_slug.startswith('my-custom-institute')
#         self.assertTrue(starts_with)
#
#     def test_string_representation_institute_model(self):
#         """Test string representation of institute model"""
#         user = create_teacher()
#         payload = {
#             'user': user,
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.SCHOOL
#         }
#         res = models.Institute.objects.create(**payload)
#         self.assertEqual(str(res), payload['name'].lower())
#
#     def test_admin_is_created_for_institute_automatically(self):
#         """
#         Test that owner is set as admin automatically
#         """
#         user = create_teacher()
#         institute = create_institute(user)
#         self.assertTrue(models.InstitutePermission.objects.filter(
#             institute=institute,
#             invitee=user,
#             role=models.InstituteRole.ADMIN,
#             active=True
#         ).exists())
#
#
# class InstituteProfileModelTests(TestCase):
#     """Tests for institute profile model."""
#
#     def test_teacher_create_institute_profile_full_details(self):
#         """
#         Test that creation of institute profile is
#         successful for teacher with full details.
#         """
#         payload = {
#             'user': create_teacher(),
#             'name': 'My Custom Institute12',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.COLLEGE,
#             'institute_profile': {
#                 'motto': 'This is custom moto.',
#                 'email': 'xyz@gmail.com',
#                 'phone': '+918787878787',
#                 'website_url': 'https://www.google.com',
#                 'state': 'TR',
#                 'address': 'xyz road',
#                 'pin': '799250',
#                 'recognition': 'ICSE'
#             }
#         }
#         institute_profile = payload['institute_profile']
#         res = models.Institute.objects.create(
#             user=payload['user'],
#             name=payload['name'],
#             institute_category=payload['institute_category'],
#             type=payload['type']
#         )
#
#         res.institute_profile.motto = institute_profile['motto']
#         res.institute_profile.email = institute_profile['email']
#         res.institute_profile.phone = institute_profile['phone']
#         res.institute_profile.website_url = institute_profile['website_url']
#         res.institute_profile.state = institute_profile['state']
#         res.institute_profile.address = institute_profile['address']
#         res.institute_profile.pin = institute_profile['pin']
#         res.institute_profile.recognition = institute_profile['recognition']
#         res.save()
#
#         res1 = models.InstituteProfile.objects.get(institute=res)
#
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#         self.assertEqual(res1.motto, institute_profile['motto'])
#         self.assertEqual(res1.email, institute_profile['email'])
#         self.assertEqual(res1.phone, institute_profile['phone'])
#         self.assertEqual(res1.website_url, institute_profile['website_url'])
#         self.assertEqual(res1.state, institute_profile['state'])
#         self.assertEqual(res1.address, institute_profile['address'])
#         self.assertEqual(res1.pin, institute_profile['pin'])
#         self.assertEqual(res1.recognition, institute_profile['recognition'])
#
#     def test_institute_profile_string_representation(self):
#         """Test that institute profile is correctly represented"""
#         user = create_teacher()
#         payload = {
#             'user': user,
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
#             'type': models.InstituteType.COLLEGE,
#         }
#         institute = models.Institute.objects.create(**payload)
#         institute_profile = models.InstituteProfile.objects.get(
#             institute=institute)
#         self.assertEqual(str(institute_profile), str(institute))
#
#     @patch('uuid.uuid4')
#     def test_institute_image_upload_url_uuid(self, mock_url):
#         """Test that institute image is uploaded in correct location"""
#         uuid = 'test-uuid'
#         mock_url.return_value = uuid
#         file_path = models.institute_logo_upload_file_path(
#             None, 'img.jpg')
#         dt = datetime.date.today()
#         path = 'pictures/uploads/institute/logo'
#         ini_path = f'{path}/{dt.year}/{dt.month}/{dt.day}'
#         expected_path = os.path.join(ini_path, f'{uuid}.jpg')
#         self.assertEqual(file_path, expected_path)
#
#     @patch('uuid.uuid4')
#     def test_institute_banner_upload_url_uuid(self, mock_url):
#         """Test that institute banner is uploaded in correct location"""
#         uuid = 'test-uuid'
#         mock_url.return_value = uuid
#         file_path = models.institute_banner_upload_file_path(
#             None, 'img.png'
#         )
#         dt = datetime.date.today()
#         path = 'pictures/uploads/institute/banner'
#         ini_path = f'{path}/{dt.year}/{dt.month}/{dt.day}'
#         expected_path = os.path.join(ini_path, f'{uuid}.png')
#         self.assertEqual(file_path, expected_path)
#
#
# class InstitutePermissionModelTests(TestCase):
#     """Test for institute permissions model"""
#
#     def setUp(self):
#         self.user = create_teacher('owner@gmail.com', 'owners')
#
#     def test_add_admin_by_owner_success(self):
#         """Test that admin can be added"""
#         institute = create_institute(self.user)
#         teacher = create_teacher()
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, teacher)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_add_admin_by_other_active_admin_success(self):
#         """Test that admin can add another admin"""
#         admin = create_teacher('admingf@gmai.com', 'admingf')
#         institute = create_institute(admin)
#         teacher = create_teacher()
#         role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         role.active = True
#         role.save()
#
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=teacher,
#             role=models.InstituteRole.ADMIN
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, teacher)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_only_teacher_can_be_added_as_admin(self):
#         """Test that only teacher can be added as admin"""
#         institute = create_institute(self.user)
#         student = create_student()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=student,
#                 role=models.InstituteRole.ADMIN
#                 )
#
#     def test_staff_can_not_add_admin(self):
#         """Test that staff user can not add admin"""
#         admin = create_teacher()
#         institute = create_institute(admin)
#         new_admin = create_teacher('newadmin@gmail.com', 'new_admin')
#         staff_role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         staff_role.active = True
#         staff_role.save()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=new_admin,
#                 role=models.InstituteRole.ADMIN
#             )
#
#     def test_faculty_can_not_add_admin(self):
#         """Test that faculty user can not add admin"""
#         admin = create_teacher()
#         institute = create_institute(admin)
#         new_admin = create_teacher('newadmin@gmail.com', 'new_admin')
#         faculty_role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=admin,
#             invitee=self.user,
#             role=models.InstituteRole.FACULTY
#         )
#         faculty_role.active = True
#         faculty_role.save()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=new_admin,
#                 role=models.InstituteRole.ADMIN
#             )
#
#     def test_non_admin_can_not_add_admin(self):
#         """Test that non admin can not add admin"""
#         admin = create_teacher()
#         institute = create_institute(admin)
#         invitee = create_teacher('newadmin@gmail.com', 'new_admin')
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=invitee,
#                 role=models.InstituteRole.ADMIN
#             )
#
#     def test_staff_addition_success_by_owner_admin(self):
#         """Test that owner can add staff permission"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=staff,
#             role=models.InstituteRole.STAFF
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, staff)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_staff_addition_success_by_active_admin(self):
#         """Test that active admin can add staff permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'ownedfrsdf')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         active_admin = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         active_admin.active = True
#         active_admin.save()
#
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=staff,
#             role=models.InstituteRole.STAFF
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, staff)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_staff_addition_fails_by_inactive_admin(self):
#         """Test that inactive admin can not add staff permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=staff,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_staff_addition_fails_by_inactive_staff(self):
#         """Test that inactive staff can not add staff permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=staff,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_staff_addition_fails_by_active_staff(self):
#         """Test that active staff can not add staff permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         staff = create_teacher()
#         staff_role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         staff_role.active = True
#         staff_role.save()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=staff,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_staff_addition_fails_by_anonymous(self):
#         """Test that unauthorised can not add staff permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         staff = create_teacher()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=staff,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_faculty_addition_success_by_owner(self):
#         """Test that owner can add faculty permission"""
#         institute = create_institute(self.user)
#         faculty = create_teacher()
#
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=faculty,
#             role=models.InstituteRole.FACULTY
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, faculty)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_faculty_addition_success_by_active_admin(self):
#         """Test that active admin can add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'ownedfrsdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         active_admin = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#         active_admin.active = True
#         active_admin.save()
#
#         res = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=faculty,
#             role=models.InstituteRole.FACULTY
#         )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, faculty)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_faculty_addition_fails_by_inactive_admin(self):
#         """Test that inactive admin can not add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.ADMIN
#         )
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_faculty_addition_fails_by_inactive_staff(self):
#         """Test that inactive staff can not add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.STAFF
#             )
#
#     def test_faculty_addition_success_by_active_staff(self):
#         """Test that active staff can add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         staff_role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         staff_role.active = True
#         staff_role.save()
#
#         res = models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.FACULTY
#             )
#         self.assertEqual(res.institute, institute)
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, faculty)
#         self.assertEqual(res.active, False)
#         self.assertEqual(res.request_accepted_on, None)
#
#     def test_faculty_addition_fails_by_inactive_faculty(self):
#         """Test that inactive faculty can not add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.FACULTY
#         )
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.FACULTY
#             )
#
#     def test_faculty_addition_fails_by_active_faculty(self):
#         """Test that active faculty can not add faculty permission"""
#         owner = create_teacher('ownedafr@gmail.com', 'owndferasdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#         faculty_role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=owner,
#             invitee=self.user,
#             role=models.InstituteRole.FACULTY
#         )
#         faculty_role.active = True
#         faculty_role.save()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.FACULTY
#             )
#
#     def test_faculty_addition_fails_by_anonymous(self):
#         """Test that unauthorised can not add faculty permission"""
#         owner = create_teacher('ownedfr@gmail.com', 'owndfersdf')
#         institute = create_institute(owner)
#         faculty = create_teacher()
#
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=faculty,
#                 role=models.InstituteRole.FACULTY
#             )
#
#     def test_duplicate_addition_of_role_fails(self):
#         """Test can not add admin role two times"""
#         institute = create_institute(self.user)
#         new_admin = create_teacher()
#         models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=new_admin,
#             role=models.InstituteRole.ADMIN
#         )
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=new_admin,
#                 role=models.InstituteRole.ADMIN
#             )
#
#     def test_invitee_can_accept_role(self):
#         """Test that invitee can accept role"""
#         new_owner = create_teacher()
#         institute = create_institute(new_owner)
#         role = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=new_owner,
#             invitee=self.user,
#             role=models.InstituteRole.STAFF
#         )
#         role.active = True
#         role.save()
#         role.refresh_from_db()
#         self.assertEqual(role.active, True)
#
#     def test_cannot_pre_activate_role_by_inviter(self):
#         """Test that inviter can not pre-activate role"""
#         institute = create_institute(self.user)
#         new_admin = create_teacher()
#         with self.assertRaises(PermissionDenied):
#             models.InstitutePermission.objects.create(
#                 institute=institute,
#                 inviter=self.user,
#                 invitee=new_admin,
#                 role=models.InstituteRole.ADMIN,
#                 active=True
#             )
#
#     def test_string_repr_of_institute_permission_model(self):
#         """Test the string representation"""
#         institute = create_institute(self.user)
#         new_admin = create_teacher()
#         perm = models.InstitutePermission.objects.create(
#             institute=institute,
#             inviter=self.user,
#             invitee=new_admin,
#             role=models.InstituteRole.ADMIN
#         )
#         self.assertEqual(str(perm), str(new_admin))
#
#
# class InstituteClassModelTests(TestCase):
#     """Tests for institute class"""
#
#     def setUp(self):
#         self.admin = create_teacher()
#         self.institute = create_institute(self.admin)
#
#     def test_institute_admin_create_class_successfully(self):
#         """Test that institute admin can create class successfully"""
#         res = models.InstituteClass.objects.create(
#             institute=self.institute,
#             name='Class 1'
#         )
#
#         self.assertEqual(res.name, 'class 1')
#         self.assertEqual(res.institute, self.institute)
#         self.assertTrue(len(res.class_slug) > 0)
#
#     def test_only_one_class_same_name_allowed_per_institute(self):
#         """Test that class names should be unique per institute"""
#         models.InstituteClass.objects.create(
#             institute=self.institute,
#             name='Class 1'
#         )
#
#         with self.assertRaises(Exception):
#             res = models.InstituteClass.objects.create(
#                 institute=self.institute,
#                 name='Class 1'
#             )
#
#     def test_name_required(self):
#         """Test that name is required"""
#         with self.assertRaises(ValueError):
#             models.InstituteClass.objects.create(
#                     institute=self.institute,
#                     name='   '
#             )
#
#     def test_string_representation(self):
#         """Test the string representation of the class model"""
#         res = models.InstituteClass.objects.create(
#             institute=self.institute,
#             name='Class 1'
#         )
#         self.assertEqual(str(res), 'class 1')
