from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import PermissionDenied

from core.models import InstituteLicense, InstituteLicensePlans,\
    Billing


class InstituteLicenseModelTests(TestCase):
    """Test related to institute license models"""

    def setUp(self):
        self.payload = {
            'type': InstituteLicensePlans.BASIC,
            'billing': Billing.MONTHLY,
            'cost': 2100,
            'discount': 0.0,
            'storage': 100,
            'no_of_admin': 1,
            'no_of_staff': 1,
            'no_of_faculty': 1,
            'no_of_student': 200
        }

    def test_superuser_license_creation_success(self):
        """Test that superuser can create license"""
        user = get_user_model().objects.create_superuser(
            email='abc@gmail.com',
            username='teampsuernemr',
            password='temppassword'
        )
        license = InstituteLicense.objects.create(
            user=user,
            type=self.payload['type'],
            billing=self.payload['billing'],
            cost=self.payload['cost'],      # in Rs
            storage=self.payload['storage'],    # in Gb
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student']
        )

        self.assertEqual(license.user, user)
        self.assertEqual(license.type, self.payload['type'])
        self.assertEqual(license.billing, self.payload['billing'])
        self.assertEqual(license.cost, self.payload['cost'])
        self.assertEqual(license.discount, self.payload['discount'])
        self.assertEqual(license.storage, self.payload['storage'])
        self.assertEqual(license.no_of_admin, self.payload['no_of_admin'])
        self.assertEqual(license.no_of_staff, self.payload['no_of_staff'])
        self.assertEqual(license.no_of_faculty, self.payload['no_of_faculty'])
        self.assertEqual(license.no_of_student, self.payload['no_of_student'])

    def test_teacher_can_not_create_license(self):
        """Test that teacher can not create license"""
        user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            password='temppassword',
            username='teampsdfuser',
        )
        user.is_teacher = True
        user.save()
        with self.assertRaises(PermissionDenied):
            InstituteLicense.objects.create(
                user=user,
                type=self.payload['type'],
                billing=self.payload['billing'],
                cost=self.payload['cost'],  # in Rs
                storage=self.payload['storage'],  # in Gb
                no_of_admin=self.payload['no_of_admin'],
                no_of_staff=self.payload['no_of_staff'],
                no_of_faculty=self.payload['no_of_faculty'],
                no_of_student=self.payload['no_of_student']
            )

    def test_student_can_not_create_license(self):
        """Test that student can not create license"""
        user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            username='teampsdfuser',
            password='temppassword'
        )
        user.is_student = True
        user.save()
        with self.assertRaises(PermissionDenied):
            InstituteLicense.objects.create(
                user=user,
                type=self.payload['type'],
                billing=self.payload['billing'],
                cost=self.payload['cost'],  # in Rs
                storage=self.payload['storage'],  # in Gb
                no_of_admin=self.payload['no_of_admin'],
                no_of_staff=self.payload['no_of_staff'],
                no_of_faculty=self.payload['no_of_faculty'],
                no_of_student=self.payload['no_of_student']
            )

    def test_staff_can_not_create_license(self):
        """Test that staff can not create license"""
        user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            username='teampsdfuser',
            password='temppassword'
        )
        user.is_staff = True
        user.save()
        with self.assertRaises(PermissionDenied):
            InstituteLicense.objects.create(
                user=user,
                type=self.payload['type'],
                billing=self.payload['billing'],
                cost=self.payload['cost'],  # in Rs
                storage=self.payload['storage'],  # in Gb
                no_of_admin=self.payload['no_of_admin'],
                no_of_staff=self.payload['no_of_staff'],
                no_of_faculty=self.payload['no_of_faculty'],
                no_of_student=self.payload['no_of_student']
            )

    def test_normal_user_can_not_create_license(self):
        """Test that staff can not create license"""
        user = get_user_model().objects.create_user(
            email='abc@gmail.com',
            username='teampsdfuser',
            password='temppassword'
        )
        with self.assertRaises(PermissionDenied):
            InstituteLicense.objects.create(
                user=user,
                type=self.payload['type'],
                billing=self.payload['billing'],
                cost=self.payload['cost'],  # in Rs
                storage=self.payload['storage'],  # in Gb
                no_of_admin=self.payload['no_of_admin'],
                no_of_staff=self.payload['no_of_staff'],
                no_of_faculty=self.payload['no_of_faculty'],
                no_of_student=self.payload['no_of_student']
            )
