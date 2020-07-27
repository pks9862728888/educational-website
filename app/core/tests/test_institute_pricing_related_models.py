import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from django.utils import timezone


from core.models import InstituteLicense, InstituteLicensePlans,\
    Billing, DiscussionForumBar, InstituteDiscountCoupon, Institute,\
    InstituteCategory, InstituteType, InstituteSelectedLicense,\
    InstituteLicenseOrderDetails, PaymentGateway


def create_user(email='abdfc@gmail.com', username='teampsdfuser'):
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='temppassword'
    )


def create_superuser(email='superuser@gmail.com', username='tempsuperuser'):
    return get_user_model().objects.create_superuser(
        email=email,
        username=username,
        password='temppasswosrd'
    )


def create_teacher(email='teacher23@gmail.com', username='tesampsdfuser'):
    teacher = get_user_model().objects.create_user(
        email=email,
        username=username,
        password='temppassssword'
    )
    teacher.is_teacher = True
    teacher.save()
    return teacher


def create_student(email='student23@gmail.com', username='tesamstudnser'):
    student = get_user_model().objects.create_user(
        email=email,
        username=username,
        password='temappasssword'
    )
    student.is_student = True
    student.save()
    return student


def create_institute(user, name='Temp Name ola'):
    """Creates and returns an institute"""
    return Institute.objects.create(
        user=user,
        name=name,
        institute_category=InstituteCategory.EDUCATION,
        type=InstituteType.COLLEGE
    )


# class InstituteLicenseModelTests(TestCase):
#     """Test related to institute license models"""
#
#     def setUp(self):
#         self.payload = {
#             'type': InstituteLicensePlans.BASIC,
#             'billing': Billing.MONTHLY,
#             'amount': 2100,
#             'discount_percent': 0.0,
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
#         user = create_superuser()
#         lic = InstituteLicense.objects.create(
#             user=user,
#             type=self.payload['type'],
#             billing=self.payload['billing'],
#             amount=self.payload['amount'],      # in Rs
#             storage=self.payload['storage'],    # in Gb
#             no_of_admin=self.payload['no_of_admin'],
#             no_of_staff=self.payload['no_of_staff'],
#             no_of_faculty=self.payload['no_of_faculty'],
#             no_of_student=self.payload['no_of_student'],
#             video_call_max_attendees=self.payload[
#                 'video_call_max_attendees'],
#             classroom_limit=self.payload['classroom_limit'],
#             department_limit=self.payload['department_limit'],
#             subject_limit=self.payload['subject_limit'],
#             scheduled_test=self.payload['scheduled_test'],
#             discussion_forum=self.payload['discussion_forum'],
#             LMS_exists=self.payload['LMS_exists'],
#         )
#
#         self.assertEqual(lic.user, user)
#         self.assertEqual(lic.type,
#                          self.payload['type'])
#         self.assertEqual(lic.billing,
#                          self.payload['billing'])
#         self.assertEqual(lic.amount,
#                          self.payload['amount'])
#         self.assertEqual(lic.discount_percent,
#                          self.payload['discount_percent'])
#         self.assertEqual(lic.storage,
#                          self.payload['storage'])
#         self.assertEqual(lic.no_of_admin,
#                          self.payload['no_of_admin'])
#         self.assertEqual(lic.no_of_staff,
#                          self.payload['no_of_staff'])
#         self.assertEqual(lic.no_of_faculty,
#                          self.payload['no_of_faculty'])
#         self.assertEqual(lic.no_of_student,
#                          self.payload['no_of_student'])
#         self.assertEqual(lic.video_call_max_attendees,
#                          self.payload['video_call_max_attendees'])
#         self.assertEqual(lic.classroom_limit,
#                          self.payload['classroom_limit'])
#         self.assertEqual(lic.department_limit,
#                          self.payload['department_limit'])
#         self.assertEqual(lic.subject_limit,
#                          self.payload['subject_limit'])
#         self.assertEqual(lic.scheduled_test,
#                          self.payload['scheduled_test'])
#         self.assertEqual(lic.discussion_forum,
#                          self.payload['discussion_forum'])
#         self.assertEqual(lic.LMS_exists,
#                          self.payload['LMS_exists'])
#
#     def test_teacher_can_not_create_license(self):
#         """Test that teacher can not create license"""
#         user = create_teacher()
#
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 amount=self.payload['amount'],  # in Rs
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
#         user = create_student()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 amount=self.payload['amount'],  # in Rs
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
#         user = create_user()
#         user.is_staff = True
#         user.save()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 amount=self.payload['amount'],  # in Rs
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
#         user = create_user()
#         with self.assertRaises(PermissionDenied):
#             InstituteLicense.objects.create(
#                 user=user,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 amount=self.payload['amount'],  # in Rs
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
#
# class TestInstituteDiscountCouponModel(TestCase):
#     """Test that institute discount coupon model works"""
#
#     def test_create_coupon_success_by_staff(self):
#         """"Test that staff can create discount coupon"""
#         staff = create_user()
#         staff.is_staff = True
#         staff.save()
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         coupon = InstituteDiscountCoupon.objects.create(
#             discount_rs=200,
#             expiry_date=expiry_date,
#             user=staff
#         )
#         self.assertEqual(coupon.discount_rs, 200)
#         self.assertEqual(coupon.expiry_date, expiry_date)
#         self.assertTrue(coupon.coupon_code.startswith('I'))
#         self.assertEqual(coupon.user, staff)
#         self.assertEqual(coupon.active, True)
#
#     def test_create_coupon_success_by_superuser(self):
#         """"Test that superuser can create discount coupon"""
#         superuser = create_superuser()
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         coupon = InstituteDiscountCoupon.objects.create(
#             discount_rs=200,
#             expiry_date=expiry_date,
#             user=superuser
#         )
#         self.assertEqual(coupon.discount_rs, 200)
#         self.assertEqual(coupon.expiry_date, expiry_date)
#         self.assertTrue(coupon.coupon_code.startswith('I'))
#         self.assertEqual(coupon.user, superuser)
#         self.assertEqual(coupon.active, True)
#
#     def test_create_coupon_fails_by_teacher(self):
#         """"Test that teacher can not create discount coupon"""
#         teacher = create_teacher()
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(PermissionDenied):
#             InstituteDiscountCoupon.objects.create(
#                 discount_rs=200,
#                 expiry_date=expiry_date,
#                 user=teacher
#             )
#
#     def test_create_coupon_fails_by_student(self):
#         """"Test that student can not create discount coupon"""
#         student = create_student()
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(PermissionDenied):
#             InstituteDiscountCoupon.objects.create(
#                 discount_rs=200,
#                 expiry_date=expiry_date,
#                 user=student
#             )
#
#     def test_create_coupon_fails_by_normal_user(self):
#         """"Test that user can not create discount coupon"""
#         user = create_user()
#
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(PermissionDenied):
#             InstituteDiscountCoupon.objects.create(
#                 discount_rs=200,
#                 expiry_date=expiry_date,
#                 user=user
#             )
#
#     def test_create_coupon_user_required(self):
#         """"Test that user is required to be provided for coupon"""
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(ValueError):
#             InstituteDiscountCoupon.objects.create(
#                 discount_rs=200,
#                 expiry_date=expiry_date
#             )
#
#     def test_discount_is_required(self):
#         """"
#         Test that user can not create discount coupon
#         without providing discount field
#         """
#         superuser = create_superuser()
#
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(ValueError):
#             InstituteDiscountCoupon.objects.create(
#                 expiry_date=expiry_date,
#                 user=superuser
#             )
#
#     def test_expiry_date_is_required(self):
#         """"
#         Test that user can not create discount coupon
#         without providing expiry date
#         """
#         superuser = create_superuser()
#         expiry_date = timezone.now() + datetime.timedelta(days=365)
#
#         with self.assertRaises(ValueError):
#             InstituteDiscountCoupon.objects.create(
#                 discount_rs=123,
#                 user=superuser
#             )
#
#
# class InstituteSelectedLicenseModelTests(TestCase):
#     """Tests for institute selected model"""
#
#     def setUp(self):
#         self.admin = create_teacher()
#         self.institute = create_institute(self.admin)
#         superuser = create_superuser()
#         self.coupon_active = InstituteDiscountCoupon.objects.create(
#             user=superuser,
#             discount_rs=123,
#             expiry_date=timezone.now() + datetime.timedelta(days=365)
#         )
#         self.coupon_inactive = InstituteDiscountCoupon.objects.create(
#             user=superuser,
#             discount_rs=123,
#             expiry_date=timezone.now() + datetime.timedelta(days=365),
#             active=False
#         )
#         self.payload = {
#             'type': InstituteLicensePlans.BASIC,
#             'billing': Billing.MONTHLY,
#             'amount': 2100,
#             'discount_percent': 0.0,
#             'discount_coupon': self.coupon_active.pk,
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
#     def test_can_select_license_without_coupon(self):
#         """Test that select license without license success"""
#         res = InstituteSelectedLicense.objects.create(
#             institute=self.institute,
#             type=self.payload['type'],
#             billing=self.payload['billing'],
#             amount=self.payload['amount'],
#             discount_percent=self.payload['discount_percent'],
#             storage=self.payload['storage'],
#             no_of_admin=self.payload['no_of_admin'],
#             no_of_staff=self.payload['no_of_staff'],
#             no_of_faculty=self.payload['no_of_faculty'],
#             no_of_student=self.payload['no_of_student'],
#             video_call_max_attendees=self.payload[
#                 'video_call_max_attendees'],
#             classroom_limit=self.payload['classroom_limit'],
#             department_limit=self.payload['department_limit'],
#             subject_limit=self.payload['subject_limit'],
#             scheduled_test=self.payload['scheduled_test'],
#             discussion_forum=self.payload['discussion_forum'],
#             LMS_exists=self.payload['LMS_exists']
#         )
#
#         self.assertEqual(res.institute, self.institute)
#         self.assertEqual(res.type, self.payload['type'])
#         self.assertEqual(res.billing,
#                          self.payload['billing'])
#         self.assertEqual(res.amount,
#                          self.payload['amount'])
#         self.assertEqual(res.discount_percent,
#                          self.payload['discount_percent'])
#         self.assertEqual(res.storage,
#                          self.payload['storage'])
#         self.assertEqual(res.no_of_admin,
#                          self.payload['no_of_admin'])
#         self.assertEqual(res.no_of_staff,
#                          self.payload['no_of_staff'])
#         self.assertEqual(res.no_of_faculty,
#                          self.payload['no_of_faculty'])
#         self.assertEqual(res.no_of_student,
#                          self.payload['no_of_student'])
#         self.assertEqual(res.video_call_max_attendees,
#                          self.payload['video_call_max_attendees'])
#         self.assertEqual(res.classroom_limit,
#                          self.payload['classroom_limit'])
#         self.assertEqual(res.department_limit,
#                          self.payload['department_limit'])
#         self.assertEqual(res.subject_limit,
#                          self.payload['subject_limit'])
#         self.assertEqual(res.scheduled_test,
#                          self.payload['scheduled_test'])
#         self.assertEqual(res.discussion_forum,
#                          self.payload['discussion_forum'])
#         self.assertEqual(res.LMS_exists,
#                          self.payload['LMS_exists'])
#         self.assertEqual(
#             res.net_amount,
#             self.payload['amount'] * (
#                     1 - self.payload['discount_percent'] / 100))
#
#     def test_can_select_license_with_active_coupon(self):
#         """Test that select license with valid coupon success"""
#         res = InstituteSelectedLicense.objects.create(
#             institute=self.institute,
#             type=self.payload['type'],
#             billing=self.payload['billing'],
#             amount=self.payload['amount'],
#             discount_percent=self.payload['discount_percent'],
#             discount_coupon=self.coupon_active,
#             storage=self.payload['storage'],
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
#             LMS_exists=self.payload['LMS_exists']
#         )
#
#         self.assertEqual(res.institute, self.institute)
#         self.assertEqual(res.type, self.payload['type'])
#         self.assertEqual(res.billing,
#                          self.payload['billing'])
#         self.assertEqual(res.amount,
#                          self.payload['amount'])
#         self.assertEqual(res.discount_percent,
#                          self.payload['discount_percent'])
#         self.assertEqual(res.storage,
#                          self.payload['storage'])
#         self.assertEqual(res.no_of_admin,
#                          self.payload['no_of_admin'])
#         self.assertEqual(res.no_of_staff,
#                          self.payload['no_of_staff'])
#         self.assertEqual(res.no_of_faculty,
#                          self.payload['no_of_faculty'])
#         self.assertEqual(res.no_of_student,
#                          self.payload['no_of_student'])
#         self.assertEqual(res.video_call_max_attendees,
#                          self.payload['video_call_max_attendees'])
#         self.assertEqual(res.classroom_limit,
#                          self.payload['classroom_limit'])
#         self.assertEqual(res.department_limit,
#                          self.payload['department_limit'])
#         self.assertEqual(res.subject_limit,
#                          self.payload['subject_limit'])
#         self.assertEqual(res.scheduled_test,
#                          self.payload['scheduled_test'])
#         self.assertEqual(res.discussion_forum,
#                          self.payload['discussion_forum'])
#         self.assertEqual(res.LMS_exists,
#                          self.payload['LMS_exists'])
#         self.assertEqual(
#             res.net_amount,
#             max(0, self.payload['amount'] * (
#                     1 - self.payload['discount_percent'] / 100) -
#                 self.coupon_active.discount_rs)
#         )
#         self.coupon_active.refresh_from_db()
#         self.assertEqual(self.coupon_active.active, False)
#
#     def test_can_select_license_with_active_coupon_free(self):
#         """Test that select license with valid coupon 0 payment"""
#         res = InstituteSelectedLicense.objects.create(
#             institute=self.institute,
#             type=self.payload['type'],
#             billing=self.payload['billing'],
#             amount=10,
#             discount_percent=self.payload['discount_percent'],
#             discount_coupon=self.coupon_active,
#             storage=self.payload['storage'],
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
#             LMS_exists=self.payload['LMS_exists']
#         )
#
#         self.assertEqual(res.net_amount, 0)
#
#     def test_cannot_select_license_with_inactive_coupon(self):
#         """Test that select license with invalid coupon fails"""
#         with self.assertRaises(ValueError):
#             InstituteSelectedLicense.objects.create(
#                 institute=self.institute,
#                 type=self.payload['type'],
#                 billing=self.payload['billing'],
#                 amount=self.payload['amount'],
#                 discount_percent=self.payload['discount_percent'],
#                 discount_coupon=self.coupon_inactive.pk,
#                 storage=self.payload['storage'],
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
#                 LMS_exists=self.payload['LMS_exists']
#             )
#
#
# class InstituteOrderTests(TestCase):
#     """Tests related to institute order table"""
#
#     def setUp(self):
#         self.admin = create_teacher()
#         self.institute = create_institute(self.admin)
#         self.sel_lic = InstituteSelectedLicense.objects.create(
#             institute=self.institute,
#             type=InstituteType.COLLEGE,
#             billing=Billing.MONTHLY,
#             amount=1111,
#             discount_percent=0.0,
#             storage=100,
#             no_of_admin=1,
#             no_of_staff=2,
#             no_of_faculty=3,
#             no_of_student=34,
#             video_call_max_attendees=200,
#             classroom_limit=999,
#             department_limit=999,
#             subject_limit=57,
#             scheduled_test=True,
#             discussion_forum=DiscussionForumBar.ONE_PER_SUBJECT_OR_SECTION,
#             LMS_exists=True
#         )
#
#     def test_order_creation_successful(self):
#         """Test that order can be created successfully"""
#         res = InstituteLicenseOrderDetails.objects.create(
#             selected_license=self.sel_lic,
#             institute=self.institute,
#             payment_gateway=PaymentGateway.RAZORPAY,
#             currency='INR'
#         )
#         self.assertEqual(res.amount, self.sel_lic.net_amount)
#         self.assertEqual(res.selected_license, self.sel_lic)
#         self.assertTrue(len(res.order_receipt) > 0)
#         self.assertEqual(res.institute, self.institute)
#         self.assertEqual(res.payment_gateway, PaymentGateway.RAZORPAY)
#         self.assertFalse(res.paid)
#         self.assertFalse(res.active)
#         self.assertEqual(res.start_date, None)
#         self.assertEqual(res.end_date, None)
#         self.assertTrue(len(res.order_id) > 0)
#
#     def test_payment_status_activation_success(self):
#         """Test that payment status can be activated successfully"""
#         res = InstituteLicenseOrderDetails.objects.create(
#             selected_license=self.sel_lic,
#             institute=self.institute,
#             payment_gateway=PaymentGateway.RAZORPAY,
#             currency='INR'
#         )
#         res.paid = True
#         res.save()
#
#         self.assertTrue(res.paid)
#
#     def test_activate_order_success(self):
#         """Test that payment status can be activated successfully"""
#         res = InstituteLicenseOrderDetails.objects.create(
#             selected_license=self.sel_lic,
#             institute=self.institute,
#             payment_gateway=PaymentGateway.RAZORPAY,
#             currency='INR'
#         )
#         start_date = timezone.now()
#         end_date = timezone.now() + datetime.timedelta(days=365)
#         res.paid = True
#         res.active = True
#         res.start_date = start_date
#         res.end_date = end_date
#         res.save()
#         res.refresh_from_db()
#
#         self.assertTrue(res.paid)
#         self.assertTrue(res.active)
#         self.assertEqual(res.start_date, start_date)
#         self.assertEqual(res.end_date, end_date)
