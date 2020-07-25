import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from core import models


# Urls for checking
INSTITUTE_GET_SPECIFIC_LICENSE_URL = reverse("institute:institute-license-detail")
INSTITUTE_DISCOUNT_COUPON_CHECK_URL = reverse("institute:get-discount-coupon")


def create_institute(user, institute_name='tempinstitute'):
    """Creates institute and return institute"""
    return models.Institute.objects.create(
        name=institute_name,
        user=user,
        institute_category=models.InstituteCategory.EDUCATION,
        type=models.InstituteType.COLLEGE
    )


def create_teacher(email='abc@gmail.com', username='tempusername'):
    """Creates and return teacher"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_teacher=True
    )

class AuthenticatedAdminTests(TestCase):
    """Tests for users with institute admin permissions"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            username='testusername',
            password='testpassword',
            is_teacher=True
        )
        self.superuser = get_user_model().objects.create_superuser(
            email='testsuperus@gmail.com',
            username='testusernamesup',
            password='testpasswordsip'
        )
        self.payload = {
            'type': models.InstituteLicensePlans.BUSINESS,
            'billing': models.Billing.MONTHLY,
            'amount': 2100,
            'discount_percent': 0.0,
            'storage': 100,
            'no_of_admin': 1,
            'no_of_staff': 1,
            'no_of_faculty': 1,
            'no_of_student': 200,
            'video_call_max_attendees': 100,
            'classroom_limit': 999,
            'department_limit': 999,
            'subject_limit': 999,
            'scheduled_test': True,
            'discussion_forum': models.DiscussionForumBar.ONE_PER_SUBJECT,
            'LMS_exists': True
        }
        self.license = models.InstituteLicense.objects.create(
            user=self.superuser,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],  # in Rs
            storage=self.payload['storage'],  # in Gb
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload['video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            discussion_forum=self.payload['discussion_forum'],
            LMS_exists=self.payload['LMS_exists'],
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # def test_admin_get_institute_selected_license_details_success(self):
    #     """Test that admin can get license details"""
    #     create_institute(self.user)
    #
    #     res = self.client.post(
    #         INSTITUTE_GET_SPECIFIC_LICENSE_URL, {'id': self.license.id})
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['billing'],
    #                      self.payload['billing'])
    #     self.assertEqual(res.data['amount'],
    #                      self.payload['amount'])
    #     self.assertEqual(res.data['storage'],
    #                      self.payload['storage'])
    #     self.assertEqual(res.data['no_of_admin'],
    #                      self.payload['no_of_admin'])
    #     self.assertEqual(res.data['no_of_staff'],
    #                      self.payload['no_of_staff'])
    #     self.assertEqual(res.data['no_of_faculty'],
    #                      self.payload['no_of_faculty'])
    #     self.assertEqual(res.data['no_of_student'],
    #                      self.payload['no_of_student'])
    #     self.assertEqual(res.data['video_call_max_attendees'],
    #                      self.payload['video_call_max_attendees'])
    #     self.assertEqual(res.data['classroom_limit'],
    #                      self.payload['classroom_limit'])
    #     self.assertEqual(res.data['department_limit'],
    #                      self.payload['department_limit'])
    #     self.assertEqual(res.data['subject_limit'],
    #                      self.payload['subject_limit'])
    #     self.assertEqual(res.data['scheduled_test'],
    #                      self.payload['scheduled_test'])
    #     self.assertEqual(res.data['discussion_forum'],
    #                      self.payload['discussion_forum'])
    #     self.assertEqual(res.data['LMS_exists'],
    #                      self.payload['LMS_exists'])
    #
    # def test_non_admin_can_not_get_institute_license_details(self):
    #     """Test that non admin can not get license details"""
    #     tempuser = create_teacher()
    #     create_institute(tempuser)
    #
    #     res = self.client.post(
    #         INSTITUTE_GET_SPECIFIC_LICENSE_URL, {'id': self.license.id})
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_get_invalid_license_id_fails(self):
    #     """Test that non admin can not get license details"""
    #     create_institute(self.user)
    #
    #     res = self.client.post(
    #         INSTITUTE_GET_SPECIFIC_LICENSE_URL, {'id': 5})
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_valid_coupon_code_success(self):
        """Test admin can check valid coupon code"""
        create_institute(self.user)
        coupon = models.InstituteDiscountCoupon.objects.create(
            user=self.superuser,
            discount_rs=1000,
            expiry_date=timezone.now() + datetime.timedelta(days=365)
        )

        res = self.client.post(
            INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
            {'coupon_code': coupon.coupon_code}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['discount_rs'], coupon.discount_rs)
        self.assertEqual(res.data['active'], True)

    def test_check_valid_coupon_code_success_fails_staff(self):
        """Test non admin can not check valid coupon code"""
        create_institute(create_teacher())
        coupon = models.InstituteDiscountCoupon.objects.create(
            user=self.superuser,
            discount_rs=1000,
            expiry_date=timezone.now() + datetime.timedelta(days=365)
        )

        res = self.client.post(
            INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
            {'coupon_code': coupon.coupon_code}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_invalid_coupon_code_fails(self):
        """Test invalid coupon code show error"""
        create_institute(self.user)
        coupon = models.InstituteDiscountCoupon.objects.create(
            user=self.superuser,
            discount_rs=1000,
            expiry_date=timezone.now() + datetime.timedelta(days=365)
        )

        res = self.client.post(
            INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
            {'coupon_code': 'ADBSDF'}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_inactive_coupon_code_fails(self):
        """Test inactive coupon code show error"""
        create_institute(self.user)
        coupon = models.InstituteDiscountCoupon.objects.create(
            user=self.superuser,
            discount_rs=1000,
            expiry_date=timezone.now() + datetime.timedelta(days=365)
        )
        coupon.active = False
        coupon.save()

        res = self.client.post(
            INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
            {'coupon_code': coupon.coupon_code}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_expired_coupon_code_fails(self):
        """Test invalid coupon code show error"""
        create_institute(self.user)
        coupon = models.InstituteDiscountCoupon.objects.create(
            user=self.superuser,
            discount_rs=1000,
            expiry_date=timezone.now() - datetime.timedelta(days=365)
        )

        res = self.client.post(
            INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
            {'coupon_code': coupon.coupon_code}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
