import datetime
import json
import os
import sys

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
INSTITUTE_SELECT_LICENSE_URL = reverse("institute:select-license")
INSTITUTE_CREATE_ORDER_URL = reverse("institute:create-order")
RAZORPAY_CALLBACK_URL = reverse("institute:razorpay-payment-callback")


def institute_license_order_get_url(institute_slug):
    return reverse("institute:get-license-purchased",
                   kwargs={'institute_slug': institute_slug})


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

    # def test_check_valid_coupon_code_success(self):
    #     """Test admin can check valid coupon code"""
    #     create_institute(self.user)
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() + datetime.timedelta(days=365)
    #     )
    #
    #     res = self.client.post(
    #         INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
    #         {'coupon_code': coupon.coupon_code}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['discount_rs'], coupon.discount_rs)
    #     self.assertEqual(res.data['active'], True)
    #
    # def test_check_valid_coupon_code_success_fails_staff(self):
    #     """Test non admin can not check valid coupon code"""
    #     create_institute(create_teacher())
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() + datetime.timedelta(days=365)
    #     )
    #
    #     res = self.client.post(
    #         INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
    #         {'coupon_code': coupon.coupon_code}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_check_invalid_coupon_code_fails(self):
    #     """Test invalid coupon code show error"""
    #     create_institute(self.user)
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() + datetime.timedelta(days=365)
    #     )
    #
    #     res = self.client.post(
    #         INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
    #         {'coupon_code': 'ADBSDF'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_check_inactive_coupon_code_fails(self):
    #     """Test inactive coupon code show error"""
    #     create_institute(self.user)
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() + datetime.timedelta(days=365)
    #     )
    #     coupon.active = False
    #     coupon.save()
    #
    #     res = self.client.post(
    #         INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
    #         {'coupon_code': coupon.coupon_code}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_check_expired_coupon_code_fails(self):
    #     """Test invalid coupon code show error"""
    #     create_institute(self.user)
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() - datetime.timedelta(days=365)
    #     )
    #
    #     res = self.client.post(
    #         INSTITUTE_DISCOUNT_COUPON_CHECK_URL,
    #         {'coupon_code': coupon.coupon_code}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_pre_payment_processing_success_no_discount_coupon_by_admin(self):
    #     """Test saving details before payment success by admin"""
    #     institute = create_institute(self.user)
    #
    #     res = self.client.post(
    #         INSTITUTE_SELECT_LICENSE_URL,
    #         {
    #             "institute_slug": institute.institute_slug,
    #             "license_id": self.license.pk,
    #             "coupon_code": ""
    #         }
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'SUCCESS')
    #     self.assertEqual(res.data['net_amount'], self.license.amount)
    #
    #     lic = models.InstituteSelectedLicense.objects.filter(
    #         institute=institute.pk
    #     ).first()
    #     self.assertNotEqual(lic, None)
    #     self.assertEqual(lic.amount, self.license.amount)
    #     self.assertEqual(lic.discount_percent,
    #                      self.license.discount_percent)
    #     self.assertEqual(lic.discount_coupon, None)
    #     self.assertEqual(lic.net_amount, self.license.amount)
    #     self.assertEqual(lic.type, self.license.type)
    #     self.assertEqual(lic.billing, self.license.billing)
    #     self.assertEqual(lic.storage, self.license.storage)
    #     self.assertEqual(lic.no_of_admin,
    #                      self.license.no_of_admin)
    #     self.assertEqual(lic.no_of_staff,
    #                      self.license.no_of_staff)
    #     self.assertEqual(lic.no_of_faculty,
    #                      self.license.no_of_faculty)
    #     self.assertEqual(lic.no_of_student,
    #                      self.license.no_of_student)
    #     self.assertEqual(lic.video_call_max_attendees,
    #                      self.license.video_call_max_attendees)
    #     self.assertEqual(lic.classroom_limit,
    #                      self.license.classroom_limit)
    #     self.assertEqual(lic.department_limit,
    #                      self.license.department_limit)
    #     self.assertEqual(lic.subject_limit,
    #                      self.license.subject_limit)
    #     self.assertEqual(lic.scheduled_test,
    #                      self.license.scheduled_test)
    #     self.assertEqual(lic.discussion_forum,
    #                      self.license.discussion_forum)
    #     self.assertEqual(lic.LMS_exists,
    #                      self.license.LMS_exists)
    #
    # def test_pre_payment_processing_success_with_discount_coupon_by_admin(self):
    #     """Test saving details before payment success by admin"""
    #     institute = create_institute(self.user)
    #     coupon = models.InstituteDiscountCoupon.objects.create(
    #         user=self.superuser,
    #         discount_rs=1000,
    #         expiry_date=timezone.now() + datetime.timedelta(days=365)
    #     )
    #
    #     res = self.client.post(
    #         INSTITUTE_SELECT_LICENSE_URL,
    #         {
    #             "institute_slug": institute.institute_slug,
    #             "license_id": self.license.pk,
    #             "coupon_code": coupon.coupon_code
    #         }
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'SUCCESS')
    #     self.assertEqual(res.data['net_amount'], max(
    #         0, self.license.amount - coupon.discount_rs))
    #
    #     lic = models.InstituteSelectedLicense.objects.filter(
    #         institute=institute
    #     ).first()
    #
    #     self.assertNotEqual(lic, None)
    #     self.assertEqual(lic.amount, self.license.amount)
    #     self.assertEqual(
    #         lic.discount_percent,
    #         self.license.discount_percent)
    #     self.assertEqual(lic.discount_coupon, coupon)
    #     self.assertEqual(lic.net_amount, max(
    #         0, self.license.amount - coupon.discount_rs))
    #     self.assertEqual(lic.type,
    #                      self.license.type)
    #     self.assertEqual(lic.billing,
    #                      self.license.billing)
    #     self.assertEqual(lic.storage,
    #                      self.license.storage)
    #     self.assertEqual(lic.no_of_admin,
    #                      self.license.no_of_admin)
    #     self.assertEqual(lic.no_of_staff,
    #                      self.license.no_of_staff)
    #     self.assertEqual(lic.no_of_faculty,
    #                      self.license.no_of_faculty)
    #     self.assertEqual(lic.no_of_student,
    #                      self.license.no_of_student)
    #     self.assertEqual(lic.video_call_max_attendees,
    #                      self.license.video_call_max_attendees)
    #     self.assertEqual(lic.classroom_limit,
    #                      self.license.classroom_limit)
    #     self.assertEqual(lic.department_limit,
    #                      self.license.department_limit)
    #     self.assertEqual(lic.subject_limit,
    #                      self.license.subject_limit)
    #     self.assertEqual(lic.scheduled_test,
    #                      self.license.scheduled_test)
    #     self.assertEqual(lic.discussion_forum,
    #                      self.license.discussion_forum)
    #     self.assertEqual(lic.LMS_exists,
    #                      self.license.LMS_exists)
    #
    #     cpn = models.InstituteDiscountCoupon.objects.filter(
    #         coupon_code=coupon.coupon_code
    #     ).first()
    #     self.assertFalse(cpn.active)
    #
    # def test_pre_payment_processing_fails_no_discount_coupon_by_other_user(self):
    #     """Test saving details before payment fails by other user"""
    #     institute = create_institute(create_teacher())
    #
    #     res = self.client.post(
    #         INSTITUTE_SELECT_LICENSE_URL,
    #         {
    #             "institute_slug": institute.institute_slug,
    #             "license_id": self.license.pk,
    #             "coupon_code": ""
    #         }
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     lic = models.InstituteSelectedLicense.objects.filter(
    #         institute=institute.pk
    #     ).exists()
    #     self.assertFalse(lic)
    #
    # def test_pre_payment_processing_fails_invalid_institute_id(self):
    #     """Test saving details before payment success by admin"""
    #     create_institute(self.user)
    #
    #     res = self.client.post(
    #         INSTITUTE_SELECT_LICENSE_URL,
    #         {
    #             "institute_slug": "abc-asd",
    #             "license_id": self.license.pk,
    #             "coupon_code": ""
    #         }
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Invalid request.')
    #
    # def test_create_order_success_by_admin(self):
    #     """Test that creating order is successful by admin"""
    #     institute = create_institute(self.user)
    #     lic = models.InstituteSelectedLicense.objects.create(
    #         institute=institute,
    #         type=self.payload['type'],
    #         billing=self.payload['billing'],
    #         amount=self.payload['amount'],
    #         discount_percent=self.payload['discount_percent'],
    #         storage=self.payload['storage'],
    #         no_of_admin=self.payload['no_of_admin'],
    #         no_of_staff=self.payload['no_of_staff'],
    #         no_of_faculty=self.payload['no_of_faculty'],
    #         no_of_student=self.payload['no_of_student'],
    #         video_call_max_attendees=self.payload[
    #             'video_call_max_attendees'],
    #         classroom_limit=self.payload['classroom_limit'],
    #         department_limit=self.payload['department_limit'],
    #         subject_limit=self.payload['subject_limit'],
    #         scheduled_test=self.payload['scheduled_test'],
    #         LMS_exists=self.payload['LMS_exists'],
    #         discussion_forum=self.payload['discussion_forum']
    #     )
    #     res = self.client.post(
    #         INSTITUTE_CREATE_ORDER_URL,
    #         {
    #             'institute_slug': institute.institute_slug,
    #             'payment_gateway': models.PaymentGateway.RAZORPAY,
    #             'license_id': lic.pk
    #         }
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['status'], 'SUCCESS')
    #     self.assertEqual(res.data['amount'], self.payload['amount'])
    #     self.assertEqual(res.data['key_id'], os.environ.get('RAZORPAY_TEST_KEY_ID'))
    #     self.assertEqual(res.data['currency'], 'INR')
    #     self.assertEqual(res.data['email'], str(self.user))
    #     self.assertEqual(res.data['contact'], None)
    #     self.assertNotEqual(res.data['order_id'], None)
    #     self.assertIn('order_details_id', res.data)
    #
    #     order = models.InstituteLicenseOrderDetails.objects.filter(
    #         institute=institute
    #     ).first()
    #     self.assertNotEqual(order, None)
    #     self.assertEqual(order.payment_gateway,
    #                      models.PaymentGateway.RAZORPAY)
    #     self.assertEqual(order.start_date, None)
    #     self.assertEqual(order.end_date, None)
    #     self.assertFalse(order.paid)
    #     self.assertFalse(order.active)
    #     self.assertEqual(res.data['order_details_id'], order.pk)
    #
    # def test_create_order_fails_by_other_user(self):
    #     """Test that creating order fails by non admin"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = models.InstituteSelectedLicense.objects.create(
    #         institute=institute,
    #         type=self.payload['type'],
    #         billing=self.payload['billing'],
    #         amount=self.payload['amount'],
    #         discount_percent=self.payload['discount_percent'],
    #         storage=self.payload['storage'],
    #         no_of_admin=self.payload['no_of_admin'],
    #         no_of_staff=self.payload['no_of_staff'],
    #         no_of_faculty=self.payload['no_of_faculty'],
    #         no_of_student=self.payload['no_of_student'],
    #         video_call_max_attendees=self.payload[
    #             'video_call_max_attendees'],
    #         classroom_limit=self.payload['classroom_limit'],
    #         department_limit=self.payload['department_limit'],
    #         subject_limit=self.payload['subject_limit'],
    #         scheduled_test=self.payload['scheduled_test'],
    #         LMS_exists=self.payload['LMS_exists'],
    #         discussion_forum=self.payload['discussion_forum']
    #     )
    #     res = self.client.post(
    #         INSTITUTE_CREATE_ORDER_URL,
    #         {
    #             'institute_slug': institute.institute_slug,
    #             'payment_gateway': models.PaymentGateway.RAZORPAY,
    #             'license_id': lic.pk
    #         }
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Insufficient permission.')
    #
    #     order = models.InstituteLicenseOrderDetails.objects.filter(
    #         institute=institute
    #     ).first()
    #     self.assertEqual(order, None)
    #
    # def test_callback_url_post_success(self):
    #     """Test that post data into callback url success"""
    #     institute = create_institute(self.user)
    #     lic = models.InstituteSelectedLicense.objects.create(
    #         institute=institute,
    #         type=self.payload['type'],
    #         billing=self.payload['billing'],
    #         amount=self.payload['amount'],
    #         discount_percent=self.payload['discount_percent'],
    #         storage=self.payload['storage'],
    #         no_of_admin=self.payload['no_of_admin'],
    #         no_of_staff=self.payload['no_of_staff'],
    #         no_of_faculty=self.payload['no_of_faculty'],
    #         no_of_student=self.payload['no_of_student'],
    #         video_call_max_attendees=self.payload[
    #             'video_call_max_attendees'],
    #         classroom_limit=self.payload['classroom_limit'],
    #         department_limit=self.payload['department_limit'],
    #         subject_limit=self.payload['subject_limit'],
    #         scheduled_test=self.payload['scheduled_test'],
    #         LMS_exists=self.payload['LMS_exists'],
    #         discussion_forum=self.payload['discussion_forum']
    #     )
    #     order = models.InstituteLicenseOrderDetails.objects.create(
    #         institute=institute,
    #         payment_gateway=models.PaymentGateway.RAZORPAY,
    #         selected_license=lic
    #     )
    #     payload = {
    #         'razorpay_order_id': 'order_FJksdhflkshfkshfs',
    #         'razorpay_payment_id': 'pay_FJlsjdfkljslfjljf',
    #         'razorpay_signature': 'lkkjslfjsljfsljfsljljs'
    #     }
    #     res = self.client.post(
    #         RAZORPAY_CALLBACK_URL,
    #         {
    #             'razorpay_order_id': payload['razorpay_order_id'],
    #             'razorpay_payment_id': payload['razorpay_payment_id'],
    #             'razorpay_signature': payload['razorpay_signature'],
    #             'order_details_id': order.pk
    #         }
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], 'FAILURE')

    def test_get_active_institute_license_details_success_by_admin(self):
        """Test that get active institute license successful by admin"""
        institute = create_institute(self.user)
        lic = models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],
            discount_percent=self.payload['discount_percent'],
            storage=self.payload['storage'],
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload[
                'video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            LMS_exists=self.payload['LMS_exists'],
            discussion_forum=self.payload['discussion_forum']
        )
        order = models.InstituteLicenseOrderDetails.objects.create(
            selected_license=lic,
            institute=institute,
            payment_gateway=models.PaymentGateway.RAZORPAY,
            currency='INR'
        )
        order.paid = True
        order.active = True
        order.end_date = timezone.now() + datetime.timedelta(
            days=364)
        order.save()
        res = self.client.get(
            institute_license_order_get_url(
                institute.institute_slug)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('active_license', res.data)
        self.assertIn('purchased_inactive_license', res.data)
        self.assertIn('expired_license', res.data)
        self.assertEqual(
            res.data['active_license'][
                'payment_date'], str(order.payment_date))
        self.assertEqual(
            res.data['active_license'][
                'start_date'], str(order.start_date))
        self.assertEqual(
            res.data['active_license'][
                'end_date'], str(order.end_date))
        self.assertEqual(
            res.data['active_license'][
                'license_details']['id'], order.selected_license.id)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['type'], order.selected_license.type)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['billing'], order.selected_license.billing)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['storage'], order.selected_license.storage)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['net_amount'], order.selected_license.net_amount)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['no_of_admin'], order.selected_license.no_of_admin)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['no_of_staff'], order.selected_license.no_of_staff)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['no_of_faculty'], order.selected_license.no_of_faculty)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['no_of_student'], order.selected_license.no_of_student)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['video_call_max_attendees'], order.selected_license.video_call_max_attendees)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['classroom_limit'], order.selected_license.classroom_limit)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['department_limit'], order.selected_license.department_limit)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['discussion_forum'], order.selected_license.discussion_forum)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['LMS_exists'], order.selected_license.LMS_exists)
        self.assertEqual(
            res.data['active_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)
        self.assertEqual(res.data['purchased_inactive_license'], {})
        self.assertEqual(res.data['expired_license'], {})

    def test_get_inactive_institute_license_details_success_by_admin(self):
        """Test that get inactive institute license successful by admin"""
        institute = create_institute(self.user)
        lic = models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],
            discount_percent=self.payload['discount_percent'],
            storage=self.payload['storage'],
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload[
                'video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            LMS_exists=self.payload['LMS_exists'],
            discussion_forum=self.payload['discussion_forum']
        )
        order = models.InstituteLicenseOrderDetails.objects.create(
            selected_license=lic,
            institute=institute,
            payment_gateway=models.PaymentGateway.RAZORPAY,
            currency='INR'
        )
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        res = self.client.get(
            institute_license_order_get_url(
                institute.institute_slug)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('active_license', res.data)
        self.assertIn('purchased_inactive_license', res.data)
        self.assertIn('expired_license', res.data)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'payment_date'], str(order.payment_date))
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['id'], order.selected_license.id)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['type'], order.selected_license.type)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['billing'], order.selected_license.billing)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['storage'], order.selected_license.storage)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['net_amount'], order.selected_license.net_amount)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['no_of_admin'], order.selected_license.no_of_admin)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['no_of_staff'], order.selected_license.no_of_staff)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['no_of_faculty'], order.selected_license.no_of_faculty)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['no_of_student'], order.selected_license.no_of_student)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['video_call_max_attendees'], order.selected_license.video_call_max_attendees)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['classroom_limit'], order.selected_license.classroom_limit)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['department_limit'], order.selected_license.department_limit)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['discussion_forum'], order.selected_license.discussion_forum)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['LMS_exists'], order.selected_license.LMS_exists)
        self.assertEqual(
            res.data['purchased_inactive_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)

        self.assertEqual(res.data['active_license'], {})
        self.assertEqual(res.data['expired_license'], {})

    def test_get_expired_institute_license_details_success_by_admin(self):
        """Test that get expired institute license successful by admin"""
        institute = create_institute(self.user)
        lic = models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],
            discount_percent=self.payload['discount_percent'],
            storage=self.payload['storage'],
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload[
                'video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            LMS_exists=self.payload['LMS_exists'],
            discussion_forum=self.payload['discussion_forum']
        )
        order = models.InstituteLicenseOrderDetails.objects.create(
            selected_license=lic,
            institute=institute,
            payment_gateway=models.PaymentGateway.RAZORPAY,
            currency='INR'
        )
        order.paid = True
        order.payment_date = timezone.now()
        order.start_date = timezone.now() - datetime.timedelta(
            days=364)
        order.end_date = timezone.now() - datetime.timedelta(
            days=1)
        order.save()
        res = self.client.get(
            institute_license_order_get_url(
                institute.institute_slug)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('active_license', res.data)
        self.assertIn('purchased_inactive_license', res.data)
        self.assertIn('expired_license', res.data)
        self.assertEqual(
            res.data['expired_license'][
                'payment_date'], str(order.payment_date))
        self.assertEqual(
            res.data['expired_license'][
                'start_date'], str(order.start_date))
        self.assertEqual(
            res.data['expired_license'][
                'end_date'], str(order.end_date))
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['id'], order.selected_license.id)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['type'], order.selected_license.type)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['billing'], order.selected_license.billing)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['storage'], order.selected_license.storage)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['net_amount'], order.selected_license.net_amount)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['no_of_admin'], order.selected_license.no_of_admin)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['no_of_staff'], order.selected_license.no_of_staff)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['no_of_faculty'], order.selected_license.no_of_faculty)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['no_of_student'], order.selected_license.no_of_student)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['video_call_max_attendees'], order.selected_license.video_call_max_attendees)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['classroom_limit'], order.selected_license.classroom_limit)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['department_limit'], order.selected_license.department_limit)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['discussion_forum'], order.selected_license.discussion_forum)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['LMS_exists'], order.selected_license.LMS_exists)
        self.assertEqual(
            res.data['expired_license'][
                'license_details']['scheduled_test'], order.selected_license.scheduled_test)
        self.assertEqual(res.data['active_license'], {})
        self.assertEqual(res.data['purchased_inactive_license'], {})

    def test_get_institute_license_details_success_by_admin(self):
        """Test that get institute license successful by admin"""
        institute = create_institute(self.user)
        lic = models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],
            discount_percent=self.payload['discount_percent'],
            storage=self.payload['storage'],
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload[
                'video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            LMS_exists=self.payload['LMS_exists'],
            discussion_forum=self.payload['discussion_forum']
        )
        res = self.client.get(
            institute_license_order_get_url(
                institute.institute_slug)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('active_license', res.data)
        self.assertIn('purchased_inactive_license', res.data)
        self.assertIn('expired_license', res.data)
        self.assertEqual(res.data['active_license'], {})
        self.assertEqual(res.data['expired_license'], {})
        self.assertEqual(res.data['purchased_inactive_license'], {})

    def test_get_expired_institute_license_details_fails_by_non_admin(self):
        """Test that get expired institute license fails for non admin"""
        admin = create_teacher()
        institute = create_institute(admin)
        lic = models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=self.payload['type'],
            billing=self.payload['billing'],
            amount=self.payload['amount'],
            discount_percent=self.payload['discount_percent'],
            storage=self.payload['storage'],
            no_of_admin=self.payload['no_of_admin'],
            no_of_staff=self.payload['no_of_staff'],
            no_of_faculty=self.payload['no_of_faculty'],
            no_of_student=self.payload['no_of_student'],
            video_call_max_attendees=self.payload[
                'video_call_max_attendees'],
            classroom_limit=self.payload['classroom_limit'],
            department_limit=self.payload['department_limit'],
            subject_limit=self.payload['subject_limit'],
            scheduled_test=self.payload['scheduled_test'],
            LMS_exists=self.payload['LMS_exists'],
            discussion_forum=self.payload['discussion_forum']
        )
        order = models.InstituteLicenseOrderDetails.objects.create(
            selected_license=lic,
            institute=institute,
            payment_gateway=models.PaymentGateway.RAZORPAY,
            currency='INR'
        )
        order.paid = True
        order.start_date = timezone.now() - datetime.timedelta(
            days=364)
        order.end_date = timezone.now() - datetime.timedelta(
            days=1)
        order.save()
        res = self.client.get(
            institute_license_order_get_url(
                institute.institute_slug)
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Insufficient permission.')
