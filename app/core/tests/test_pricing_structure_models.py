# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.core.exceptions import PermissionDenied
#
# from core.models import InstituteLicense, InstituteLicensePlans,\
#     Billing, DiscussionForumBar
#
#
# class InstituteLicenseModelTests(TestCase):
#     """Test related to institute license models"""
#
#     def setUp(self):
#         self.payload = {
#             'type': InstituteLicensePlans.BASIC,
#             'billing': Billing.MONTHLY,
#             'cost': 2100,
#             'discount': 0.0,
#             'storage': 100,
#             'no_of_admin': 1,
#             'no_of_staff': 1,
#             'no_of_faculty': 1,
#             'no_of_student': 200,
#             'video_call_max_attendees': 100,
#             'classroom_limit': 999,
#             'department_limit': 999,
#             'subject_limit': 999,
#             'scheduled_test': True,
#             'discussion_forum': DiscussionForumBar.ONE_PER_SUBJECT,
#             'LMS_exists': True
#         }
#
#     def test_superuser_license_creation_success(self):
#         """Test that superuser can create license"""
#         user = get_user_model().objects.create_superuser(
#             email='abc@gmail.com',
#             username='teampsuernemr',
#             password='temppassword'
#         )
#         license = InstituteLicense.objects.create(
#             user=user,
#             type=self.payload['type'],
#             billing=self.payload['billing'],
#             cost=self.payload['cost'],      # in Rs
#             storage=self.payload['storage'],    # in Gb
#             no_of_admin=self.payload['no_of_admin'],
#             no_of_staff=self.payload['no_of_staff'],
#             no_of_faculty=self.payload['no_of_faculty'],
#             no_of_student=self.payload['no_of_student'],
#             video_call_max_attendees=self.payload['video_call_max_attendees'],
#             classroom_limit=self.payload['classroom_limit'],
#             department_limit=self.payload['department_limit'],
#             subject_limit=self.payload['subject_limit'],
#             scheduled_test=self.payload['scheduled_test'],
#             discussion_forum=self.payload['discussion_forum'],
#             LMS_exists=self.payload['LMS_exists'],
#         )
#
#         self.assertEqual(license.user, user)
#         self.assertEqual(license.type, self.payload['type'])
#         self.assertEqual(license.billing, self.payload['billing'])
#         self.assertEqual(license.cost, self.payload['cost'])
#         self.assertEqual(license.discount, self.payload['discount'])
#         self.assertEqual(license.storage, self.payload['storage'])
#         self.assertEqual(license.no_of_admin, self.payload['no_of_admin'])
#         self.assertEqual(license.no_of_staff, self.payload['no_of_staff'])
#         self.assertEqual(license.no_of_faculty, self.payload['no_of_faculty'])
#         self.assertEqual(license.no_of_student, self.payload['no_of_student'])
#         self.assertEqual(license.video_call_max_attendees, self.payload['video_call_max_attendees'])
#         self.assertEqual(license.classroom_limit, self.payload['classroom_limit'])
#         self.assertEqual(license.department_limit, self.payload['department_limit'])
#         self.assertEqual(license.subject_limit, self.payload['subject_limit'])
#         self.assertEqual(license.scheduled_test, self.payload['scheduled_test'])
#         self.assertEqual(license.discussion_forum, self.payload['discussion_forum'])
#         self.assertEqual(license.LMS_exists, self.payload['LMS_exists'])
#
#     def test_teacher_can_not_create_license(self):
#         """Test that teacher can not create license"""
#         user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             password='temppassword',
#             username='teampsdfuser',
#         )
#         user.is_teacher = True
#         user.save()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 cost=self.payload['cost'],  # in Rs
#                 storage=self.payload['storage'],  # in Gb
#                 no_of_admin=self.payload['no_of_admin'],
#                 no_of_staff=self.payload['no_of_staff'],
#                 no_of_faculty=self.payload['no_of_faculty'],
#                 no_of_student=self.payload['no_of_student'],
#                 video_call_max_attendees=self.payload['video_call_max_attendees'],
#                 classroom_limit=self.payload['classroom_limit'],
#                 department_limit=self.payload['department_limit'],
#                 subject_limit=self.payload['subject_limit'],
#                 scheduled_test=self.payload['scheduled_test'],
#                 discussion_forum=self.payload['discussion_forum'],
#                 LMS_exists=self.payload['LMS_exists'],
#             )
#
#     def test_student_can_not_create_license(self):
#         """Test that student can not create license"""
#         user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             username='teampsdfuser',
#             password='temppassword'
#         )
#         user.is_student = True
#         user.save()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 cost=self.payload['cost'],  # in Rs
#                 storage=self.payload['storage'],  # in Gb
#                 no_of_admin=self.payload['no_of_admin'],
#                 no_of_staff=self.payload['no_of_staff'],
#                 no_of_faculty=self.payload['no_of_faculty'],
#                 no_of_student=self.payload['no_of_student'],
#                 video_call_max_attendees=self.payload['video_call_max_attendees'],
#                 classroom_limit=self.payload['classroom_limit'],
#                 department_limit=self.payload['department_limit'],
#                 subject_limit=self.payload['subject_limit'],
#                 scheduled_test=self.payload['scheduled_test'],
#                 discussion_forum=self.payload['discussion_forum'],
#                 LMS_exists=self.payload['LMS_exists'],
#             )
#
#     def test_staff_can_not_create_license(self):
#         """Test that staff can not create license"""
#         user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             username='teampsdfuser',
#             password='temppassword'
#         )
#         user.is_staff = True
#         user.save()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 cost=self.payload['cost'],  # in Rs
#                 storage=self.payload['storage'],  # in Gb
#                 no_of_admin=self.payload['no_of_admin'],
#                 no_of_staff=self.payload['no_of_staff'],
#                 no_of_faculty=self.payload['no_of_faculty'],
#                 no_of_student=self.payload['no_of_student'],
#                 video_call_max_attendees=self.payload['video_call_max_attendees'],
#                 classroom_limit=self.payload['classroom_limit'],
#                 department_limit=self.payload['department_limit'],
#                 subject_limit=self.payload['subject_limit'],
#                 scheduled_test=self.payload['scheduled_test'],
#                 discussion_forum=self.payload['discussion_forum'],
#                 LMS_exists=self.payload['LMS_exists'],
#             )
#
#     def test_normal_user_can_not_create_license(self):
#         """Test that staff can not create license"""
#         user = get_user_model().objects.create_user(
#             email='abc@gmail.com',
#             username='teampsdfuser',
#             password='temppassword'
#         )
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 cost=self.payload['cost'],  # in Rs
#                 storage=self.payload['storage'],  # in Gb
#                 no_of_admin=self.payload['no_of_admin'],
#                 no_of_staff=self.payload['no_of_staff'],
#                 no_of_faculty=self.payload['no_of_faculty'],
#                 no_of_student=self.payload['no_of_student'],
#                 video_call_max_attendees=self.payload['video_call_max_attendees'],
#                 classroom_limit=self.payload['classroom_limit'],
#                 department_limit=self.payload['department_limit'],
#                 subject_limit=self.payload['subject_limit'],
#                 scheduled_test=self.payload['scheduled_test'],
#                 discussion_forum=self.payload['discussion_forum'],
#                 LMS_exists=self.payload['LMS_exists'],
#             )
