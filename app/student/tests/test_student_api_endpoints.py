# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from core import models
#
# # Urls for running the tests
# CREATE_CLASSROOM_URL = reverse("teacher:create-classroom")
# CREATE_SUBJECT_URL = reverse("teacher:create-subject")
#
#
# def create_new_user(**kwargs):
#     """Creates a new user"""
#     return get_user_model().objects.create_user(**kwargs)
#
#
# class privateStudentAPITests(TestCase):
#     """Tests for authenticated students"""
#
#     def setUp(self):
#         self.user_student = create_new_user(**{
#             'email': 'test@curesio.com',
#             'password': 'testpass@1234',
#             'username': 'testuser',
#             'is_student': True
#         })
#         self.user_teacher = create_new_user(**{
#             'email': 'tesd@curesio.com',
#             'password': 'tedtpass@1234',
#             'username': 'testduser',
#             'is_teacher': True
#         })
#         self.classroom = models.Classroom.objects.create(
#             user=self.user_teacher,
#             name='tempclassroom'
#         )
#
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user_student)
#
#     def test_create_classroom_unsuccessful(self):
#         """Test that creating classroom is unsuccessful for student"""
#         payload = {
#             'name': 'Tempclassroom'
#         }
#
#         res = self.client.post(CREATE_CLASSROOM_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_unsuccessful_classroom_url(self):
#         """Test that get is unsuccessful for student on create classroom url"""
#
#         res = self.client.get(CREATE_CLASSROOM_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_create_subject_unsuccessful(self):
#         """Test that creating subject is unsuccessful for student"""
#         payload = {
#             'classroom': self.classroom.pk,
#             'name': 'Tempsubject'
#         }
#
#         res = self.client.post(CREATE_SUBJECT_URL, payload)
#
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_get_unsuccessful_subject_url(self):
#         """Test that get is unsuccessful for student on create subject url"""
#
#         res = self.client.get(CREATE_SUBJECT_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
