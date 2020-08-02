import os
import datetime

from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from core import models
from django.core.exceptions import PermissionDenied


def create_teacher(email='teacher@gmail.com', username='tempusername'):
    """Creates and return teacher user"""
    return get_user_model().objects.create_user(
        email=email,
        password='teacherpassword',
        username=username,
        is_teacher=True
    )


def create_student(email='student@gmail.com', username='tempsdffd'):
    """Creates and return student user"""
    return get_user_model().objects.create_user(
        email=email,
        password='teacherpassword',
        username=username,
        is_student=True
    )


def create_user(email='user@gmail.com', username='usertemp'):
    """Creates and return student user"""
    return get_user_model().objects.create_user(
        email=email,
        password='teacherpassword',
        username=username
    )


def create_institute(user, name='Temp Name ola'):
    """Creates and returns an institute"""
    return models.Institute.objects.create(
        user=user,
        name=name,
        institute_category=models.InstituteCategory.EDUCATION,
        type=models.InstituteType.COLLEGE
    )


def create_class(institute, name='temp class'):
    """Creates and returns a class"""
    return models.InstituteClass.objects.create(
        institute=institute,
        name=name
    )


def create_subject(class_, name='temp class',
                   type_=models.InstituteSubjectType.MANDATORY):
    """Creates and returns a subject"""
    return models.InstituteSubject.objects.create(
        subject_class=class_,
        name=name,
        type=type_
    )


def create_section(class_, name='temp class'):
    """Creates and returns a section"""
    return models.InstituteSection.objects.create(
        section_class=class_,
        name=name
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
#             class_institute=self.institute,
#             name='Class 1'
#         )
#
#         self.assertEqual(res.name, 'class 1')
#         self.assertEqual(res.class_institute, self.institute)
#         self.assertTrue(len(res.class_slug) > 0)
#
#     def test_only_one_class_same_name_allowed_per_institute(self):
#         """Test that class names should be unique per institute"""
#         models.InstituteClass.objects.create(
#             class_institute=self.institute,
#             name='Class 1'
#         )
#
#         with self.assertRaises(Exception):
#             res = models.InstituteClass.objects.create(
#                 class_institute=self.institute,
#                 name='Class 1'
#             )
#
#     def test_name_required(self):
#         """Test that name is required"""
#         with self.assertRaises(ValueError):
#             models.InstituteClass.objects.create(
#                     class_institute=self.institute,
#                     name='   '
#             )
#
#     def test_string_representation(self):
#         """Test the string representation of the class model"""
#         res = models.InstituteClass.objects.create(
#             class_institute=self.institute,
#             name='Class 1'
#         )
#         self.assertEqual(str(res), 'class 1')
#
#
# class InstituteStatisticsModelTests(TestCase):
#     """Test that institute statistic model data is initialized to zero"""
#
#     def setUp(self):
#         self.user = create_teacher()
#         self.institute = create_institute(self.user)
#
#     def test_institute_statistics_model_is_created_when_institute_creates(self):
#         """Test that creating institute creates this model"""
#         self.assertTrue(models.InstituteStatistics.objects.filter(
#             institute=self.institute
#         ).exists())
#
#     def test_institute_statistics_model_is_initialized_to_zero(self):
#         """Test admin is 1 but others are initialized to 0"""
#         res = models.InstituteStatistics.objects.filter(
#             institute=self.institute
#         ).first()
#
#         self.assertEqual(res.no_of_admins, 1)
#         self.assertEqual(res.no_of_staffs, 0)
#         self.assertEqual(res.no_of_faculties, 0)
#         self.assertEqual(res.no_of_students, 0)
#         self.assertEqual(res.department_count, 0)
#         self.assertEqual(res.class_count, 0)
#         self.assertEqual(res.section_count, 0)
#         self.assertEqual(res.storage_count, 0.0)
#
#     def test_institute_statistics_model_update_value_success(self):
#         """Test that update statistics is success"""
#         res = models.InstituteStatistics.objects.filter(
#             institute=self.institute
#         ).first()
#         res.no_of_admins += 1
#         res.no_of_staffs += 1
#         res.no_of_faculties += 1
#         res.no_of_students += 1
#         res.department_count += 1
#         res.class_count += 1
#         res.section_count += 1
#         res.storage_count += 1
#         res.save()
#         res.refresh_from_db()
#
#         self.assertEqual(res.no_of_admins, 2)
#         self.assertEqual(res.no_of_staffs, 1)
#         self.assertEqual(res.no_of_faculties, 1)
#         self.assertEqual(res.no_of_students, 1)
#         self.assertEqual(res.department_count, 1)
#         self.assertEqual(res.class_count, 1)
#         self.assertEqual(res.section_count, 1)
#         self.assertEqual(res.storage_count, 1)
#
#
# class InstituteSubjectModelTests(TestCase):
#     """Tests related to institute subject related model"""
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='tempuserna@gmail.com',
#             password='temppass',
#             username='teampusername'
#         )
#         self.user.is_teacher = True
#         self.user.save()
#         self.payload = {
#             'name': 'Temp subject',
#             'type': models.InstituteSubjectType.MANDATORY
#         }
#
#     def test_subject_creation_success(self):
#         """Test that subject creation is success"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         res = models.InstituteSubject.objects.create(
#             subject_class=subject_class,
#             name=self.payload['name'],
#             type=self.payload['type']
#         )
#         self.assertEqual(res.subject_class.institute, institute)
#         self.assertEqual(res.subject_class, subject_class)
#         self.assertEqual(res.name, self.payload['name'].lower())
#         self.assertEqual(res.type, self.payload['type'])
#
#     def test_class_required(self):
#         """Test that class is required for subject creation"""
#         institute = create_institute(self.user)
#         with self.assertRaises(IntegrityError):
#             models.InstituteSubject.objects.create(
#                 name=self.payload['name'],
#                 type=self.payload['type']
#             )
#
#     def test_name_required(self):
#         """Test that name is required for subject creation"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         with self.assertRaises(ValueError):
#             models.InstituteSubject.objects.create(
#                 subject_class=subject_class,
#                 type=self.payload['type']
#             )
#
#     def test_type_required(self):
#         """Test that type is required for subject creation"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         with self.assertRaises(ValueError):
#             models.InstituteSubject.objects.create(
#                 subject_class=subject_class,
#                 name=self.payload['name']
#             )
#
#     def test_name_can_not_be_blank(self):
#         """Test that class name can not be blank"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         payload = {
#             'name': '   ',
#             'type': models.InstituteSubjectType.MANDATORY
#         }
#         with self.assertRaises(ValueError):
#             models.InstituteSubject.objects.create(
#                 subject_class=subject_class,
#                 name=payload['name'],
#                 type=payload['type']
#             )
#
#     def test_duplicate_subject_creation_for_same_class_fails(self):
#         """Test that duplicate class for same subject can not be done"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         models.InstituteSubject.objects.create(
#             subject_class=subject_class,
#             name=self.payload['name'],
#             type=self.payload['type']
#         )
#         with self.assertRaises(IntegrityError):
#             models.InstituteSubject.objects.create(
#                 subject_class=subject_class,
#                 name=self.payload['name'],
#                 type=self.payload['type']
#             )
#
#     def test_different_class_can_have_same_subject(self):
#         """Test that different class can contain same subject"""
#         institute = create_institute(self.user)
#         subject_class = create_class(institute)
#         class_1 = create_class(institute, 'class 1')
#         res = models.InstituteSubject.objects.create(
#             subject_class=subject_class,
#             name=self.payload['name'],
#             type=self.payload['type']
#         )
#         res1 = models.InstituteSubject.objects.create(
#             subject_class=class_1,
#             name=self.payload['name'],
#             type=self.payload['type']
#         )
#         self.assertEqual(res.name, self.payload['name'].lower())
#         self.assertEqual(res1.name, self.payload['name'].lower())
#
#
# class InstituteSectionModel(TestCase):
#     """Tests for section model"""
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='tempuser@gmail.com',
#             username='usertempname',
#             password='temppassword'
#         )
#         self.user.is_teacher = True
#         self.user.save()
#         self.payload = {'name': 'Temp subject'}
#
#     def test_section_creation_success(self):
#         """Test that section creation is successful"""
#         institute = create_institute(self.user)
#         class_ = create_class(institute)
#         res = models.InstituteSection.objects.create(
#             section_class=class_,
#             name=self.payload['name'])
#         self.assertEqual(res.section_class.institute, institute)
#         self.assertEqual(res.section_class, class_)
#         self.assertEqual(res.name, self.payload['name'].lower())
#
#     def test_class_required(self):
#         """Test that class is required for section creation"""
#         with self.assertRaises(IntegrityError):
#             models.InstituteSection.objects.create(
#                 name=self.payload['name']
#             )
#
#     def test_name_required(self):
#         """Test that name is required for section creation"""
#         institute = create_institute(self.user)
#         section_class = create_class(institute)
#         with self.assertRaises(ValueError):
#             models.InstituteSection.objects.create(
#                 section_class=section_class)
#
#     def test_name_can_not_be_blank(self):
#         """Test that section name can not be blank"""
#         institute = create_institute(self.user)
#         section_class = create_class(institute)
#         payload = {'name': '   '}
#         with self.assertRaises(ValueError):
#             models.InstituteSection.objects.create(
#                 section_class=section_class,
#                 name=payload['name']
#             )
#
#     def test_duplicate_section_creation_for_same_class_fails(self):
#         """Test that duplicate section for same class can not be done"""
#         institute = create_institute(self.user)
#         section_class = create_class(institute)
#         models.InstituteSection.objects.create(
#             section_class=section_class,
#             name=self.payload['name'])
#         with self.assertRaises(IntegrityError):
#             models.InstituteSection.objects.create(
#                 section_class=section_class,
#                 name=self.payload['name'])
#
#     def test_different_class_can_have_same_section(self):
#         """Test that different class can have same section"""
#         institute = create_institute(self.user)
#         section_class = create_class(institute)
#         class_1 = create_class(institute, 'class 1')
#         res = models.InstituteSection.objects.create(
#             section_class=section_class,
#             name=self.payload['name'])
#         res1 = models.InstituteSection.objects.create(
#             section_class=class_1,
#             name=self.payload['name'])
#         self.assertEqual(res.name, self.payload['name'].lower())
#         self.assertEqual(res1.name, self.payload['name'].lower())


# class InstituteClassPermissionTests(TestCase):
#     """
#     Tests for institute class permission model.
#     Only Admin can add Staff / Admin
#     """
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='tempuser@tgmail.com',
#             password='tempoassdfsword',
#             username='tempusernamesdfs'
#         )
#         self.user.is_teacher = True
#         self.user.save()
#
#     def test_add_staff_to_class_success_by_admin(self):
#         """Test that admin can add staff to class"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
#         accept_invite(institute, staff, models.InstituteRole.STAFF)
#         class_ = create_class(institute)
#
#         res = models.InstituteClassPermission.objects.create(
#             inviter=self.user,
#             invitee=staff,
#             to=class_
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, staff)
#         self.assertEqual(res.to, class_)
#
#     def test_add_admin_to_class_success_by_admin(self):
#         """Test that admin can add admin to class"""
#         institute = create_institute(self.user)
#         admin = create_teacher()
#         create_invite(institute, self.user, admin, models.InstituteRole.ADMIN)
#         accept_invite(institute, admin, models.InstituteRole.ADMIN)
#         class_ = create_class(institute)
#
#         res = models.InstituteClassPermission.objects.create(
#             inviter=self.user,
#             invitee=admin,
#             to=class_
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, admin)
#         self.assertEqual(res.to, class_)
#
#
# class InstituteSubjectPermissionTests(TestCase):
#     """
#     Tests for institute subject permission model.
#     Only Admin/Staff can add Staff / Admin / Faculty
#     """
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='tempuser@tgmail.com',
#             password='tempoassdfsword',
#             username='tempusernamesdfs'
#         )
#         self.user.is_teacher = True
#         self.user.save()
#
#     def test_add_staff_to_subject_success_by_admin(self):
#         """Test that admin can add staff to subject"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
#         accept_invite(institute, staff, models.InstituteRole.STAFF)
#         class_ = create_class(institute)
#         subject = create_subject(class_)
#
#         res = models.InstituteSubjectPermission.objects.create(
#             inviter=self.user,
#             invitee=staff,
#             to=subject
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, staff)
#         self.assertEqual(res.to, subject)
#
#     def test_add_admin_to_subject_success_by_admin(self):
#         """Test that admin can add admin to subject"""
#         institute = create_institute(self.user)
#         admin = create_teacher()
#         create_invite(institute, self.user, admin, models.InstituteRole.ADMIN)
#         accept_invite(institute, admin, models.InstituteRole.ADMIN)
#         class_ = create_class(institute)
#         subject = create_subject(class_)
#
#         res = models.InstituteSubjectPermission.objects.create(
#             inviter=self.user,
#             invitee=admin,
#             to=subject
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, admin)
#         self.assertEqual(res.to, subject)
#
#     def test_add_faculty_to_subject_success_by_admin(self):
#         """Test that admin can add faculty to subject"""
#         institute = create_institute(self.user)
#         faculty = create_teacher()
#         create_invite(institute, self.user, faculty, models.InstituteRole.FACULTY)
#         accept_invite(institute, faculty, models.InstituteRole.FACULTY)
#         class_ = create_class(institute)
#         subject = create_subject(class_)
#
#         res = models.InstituteSubjectPermission.objects.create(
#             inviter=self.user,
#             invitee=faculty,
#             to=subject
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, faculty)
#         self.assertEqual(res.to, subject)


# class InstituteSectionPermissionTests(TestCase):
#     """
#     Tests for institute section permission model.
#     Only Admin/Staff can add Staff / Admin
#     """
#
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='tempuser@tgmail.com',
#             password='tempoassdfsword',
#             username='tempusernamesdfs'
#         )
#         self.user.is_teacher = True
#         self.user.save()
#
#     def test_add_staff_to_section_success_by_admin(self):
#         """Test that admin can add staff to section"""
#         institute = create_institute(self.user)
#         staff = create_teacher()
#         create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
#         accept_invite(institute, staff, models.InstituteRole.STAFF)
#         class_ = create_class(institute)
#         section = create_section(class_)
#
#         res = models.InstituteSectionPermission.objects.create(
#             inviter=self.user,
#             invitee=staff,
#             to=section
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, staff)
#         self.assertEqual(res.to, section)
#
#     def test_add_admin_to_section_success_by_admin(self):
#         """Test that admin can add admin to section"""
#         institute = create_institute(self.user)
#         admin = create_teacher()
#         create_invite(institute, self.user, admin, models.InstituteRole.ADMIN)
#         accept_invite(institute, admin, models.InstituteRole.ADMIN)
#         class_ = create_class(institute)
#         section = create_section(class_)
#
#         res = models.InstituteSectionPermission.objects.create(
#             inviter=self.user,
#             invitee=admin,
#             to=section
#         )
#         self.assertEqual(res.inviter, self.user)
#         self.assertEqual(res.invitee, admin)
#         self.assertEqual(res.to, section)
