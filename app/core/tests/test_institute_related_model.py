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
#         }
#         res = models.Institute.objects.create(**payload)
#
#         self.assertTrue(models.Institute.objects.filter(
#             name=payload['name'].lower()).exists())
#         self.assertEqual(res.user, user)
#         self.assertEqual(res.name, payload['name'].lower())
#         self.assertEqual(res.institute_category, payload['institute_category'])
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
#         }
#         payload1 = {
#             'user': create_teacher('temp@gmail.com', 'newusername'),
#             'name': 'My Custom Institute',
#             'institute_category': models.InstituteCategory.EDUCATION,
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
#         }
#         res = models.Institute.objects.create(**payload)
#         self.assertEqual(str(res), payload['name'].lower())
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
#         }
#         institute = models.Institute.objects.create(**payload)
#         institute_profile = models.InstituteProfile.objects.get(
#             institute=institute)
#         self.assertEqual(str(institute_profile), str(institute))
# #
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
