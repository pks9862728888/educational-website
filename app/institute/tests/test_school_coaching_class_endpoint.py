import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core import models


INSTITUTE_ADD_CLASS_PERMISSION = reverse('institute:add-class-permission')


def get_institute_create_class_url(institute_slug):
    return reverse("institute:create-class",
                   kwargs={'institute_slug': institute_slug})


def get_institute_list_class_url(institute_slug):
    return reverse("institute:list-all-class",
                   kwargs={'institute_slug': institute_slug})


def get_institute_delete_class_url(class_slug):
    return reverse("institute:delete-class",
                   kwargs={'class_slug': class_slug})


def create_teacher(email='abc@gmail.com', username='tempusername'):
    """Creates and return teacher"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_teacher=True
    )


def create_institute(user, institute_name='tempinstitute'):
    """Creates institute and return institute"""
    return models.Institute.objects.create(
        name=institute_name,
        user=user,
        institute_category=models.InstituteCategory.EDUCATION,
        type=models.InstituteType.COLLEGE
    )


def create_institute_license(institute, payload):
    """Creates and returns institute license"""
    return models.InstituteSelectedLicense.objects.create(
            institute=institute,
            type=payload['type'],
            billing=payload['billing'],
            amount=payload['amount'],
            discount_percent=payload['discount_percent'],
            storage=payload['storage'],
            no_of_admin=payload['no_of_admin'],
            no_of_staff=payload['no_of_staff'],
            no_of_faculty=payload['no_of_faculty'],
            no_of_student=payload['no_of_student'],
            video_call_max_attendees=payload[
                'video_call_max_attendees'],
            classroom_limit=payload['classroom_limit'],
            department_limit=payload['department_limit'],
            subject_limit=payload['subject_limit'],
            scheduled_test=payload['scheduled_test'],
            LMS_exists=payload['LMS_exists'],
            discussion_forum=payload['discussion_forum'])


def create_order(license_, institute):
    """Creates and returns institute order"""
    return models.InstituteLicenseOrderDetails.objects.create(
        selected_license=license_,
        institute=institute,
        payment_gateway=models.PaymentGateway.RAZORPAY,
        currency='INR')


def create_class(institute, name='temp class'):
    """Creates and returns class"""
    class_ = models.InstituteClass.objects.create(
        class_institute=institute,
        name=name)
    stat = models.InstituteStatistics.objects.filter(
        institute=institute).first()
    stat.class_count += 1
    stat.save()
    return class_


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


def create_institute_class_permission(inviter, invitee, class_):
    """Creates and returns institute class permission"""
    return models.InstituteClassPermission.objects.create(
        inviter=inviter,
        invitee=invitee,
        to=class_
    )


class SchoolCollegeAuthenticatedTeacherTests(TestCase):
    """Tests related to creation and providing permission to class"""

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='testuser@gmail.com',
            username='testusername',
            password='testpassword'
        )
        self.user.is_teacher = True
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.payload = {
            'type': models.InstituteLicensePlans.BUSINESS,
            'billing': models.Billing.MONTHLY,
            'amount': 2100,
            'discount_percent': 0.0,
            'storage': 100,
            'no_of_admin': 1,
            'no_of_staff': 1,
            'no_of_faculty': 1,
            'no_of_student': 1,
            'video_call_max_attendees': 1,
            'classroom_limit': 1,
            'department_limit': 0,
            'subject_limit': 1,
            'scheduled_test': True,
            'discussion_forum': models.DiscussionForumBar.ONE_PER_SUBJECT,
            'LMS_exists': True
        }

    # def test_create_class_success_by_admin_after_purchasing_license(self):
    #     """Test that class creation is successful by admin user after license is purchased"""
    #     institute = create_institute(self.user)
    #     lic_ = create_institute_license(institute, self.payload)
    #     order = create_order(lic_, institute)
    #     order.paid = True
    #     order.save()
    #
    #     payload = {
    #         'name': 'Temp institute'
    #     }
    #     res = self.client.post(
    #         get_institute_create_class_url(institute.institute_slug),
    #         {'name': payload['name']})
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], payload['name'].lower())
    #     ins = models.InstituteStatistics.objects.filter(institute=institute).first()
    #     self.assertEqual(ins.class_count, 1)
    #
    # def test_class_creation_by_staff_fails(self):
    #     """Test that only admin can create class"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic_ = create_institute_license(institute, self.payload)
    #     order = create_order(lic_, institute)
    #     order.paid = True
    #     order.save()
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     payload = {
    #         'name': 'Temp institute'
    #     }
    #     res = self.client.post(
    #         get_institute_create_class_url(institute.institute_slug),
    #         {'name': payload['name']})
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_class_creation_by_faculty_fails(self):
    #     """Test that only admin can create class"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic_ = create_institute_license(institute, self.payload)
    #     order = create_order(lic_, institute)
    #     order.paid = True
    #     order.save()
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #
    #     payload = {
    #         'name': 'Temp institute'
    #     }
    #     res = self.client.post(
    #         get_institute_create_class_url(institute.institute_slug),
    #         {'name': payload['name']})
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_create_class_limit_exceed_fails(self):
    #     """Test that can only create class within limit is allowed"""
    #     institute = create_institute(self.user)
    #     lic_ = create_institute_license(institute, self.payload)
    #     order = create_order(lic_, institute)
    #     order.paid = True
    #     order.save()
    #
    #     payload = {
    #         'name': 'Temp institute'
    #     }
    #     self.client.post(
    #         get_institute_create_class_url(institute.institute_slug),
    #         {'name': payload['name']})
    #     res = res = self.client.post(
    #         get_institute_create_class_url(institute.institute_slug),
    #         {'name': 'Temp class X'})
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Maximum class creation limit attained.')
    #
    # def test_get_all_class_when_no_class_created_success_by_permitted_user(self):
    #     """Test list all class success by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     res = self.client.get(
    #         get_institute_list_class_url(institute.institute_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_get_all_class_when_class_created_success_by_permitted_user(self):
    #     """Test list all class success by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     res = self.client.get(
    #         get_institute_list_class_url(institute.institute_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], class_.name)
    #     self.assertEqual(res.data[0]['class_slug'], class_.class_slug)
    #
    # def test_get_all_class_fails_by_unpermitted_user(self):
    #     """Test list all class fails by unpermitted user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     create_class(institute)
    #     res = self.client.get(
    #         get_institute_list_class_url(institute.institute_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_class_success_by_admin(self):
    #     """Test that admin can delete class"""
    #     create_institute(self.user, 'sdfsdff')
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.delete(
    #         get_institute_delete_class_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.InstituteClass.objects.filter(
    #         class_slug=class_.class_slug
    #     ).exists())
    #     self.assertEqual(models.InstituteStatistics.objects.filter(
    #         institute=institute
    #     ).first().class_count, 0)
    #
    # def test_delete_class_success_by_permitted_staff(self):
    #     """Test that admin can delete class"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.delete(
    #         get_institute_delete_class_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.InstituteClass.objects.filter(
    #         class_slug=class_.class_slug
    #     ).exists())
    #     self.assertEqual(models.InstituteStatistics.objects.filter(
    #         institute=institute
    #     ).first().class_count, 0)
    #
    # def test_delete_class_fails_by_non_admin(self):
    #     """Test that admin can delete class"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.delete(
    #         get_institute_delete_class_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')

    def test_provide_class_permission_to_staff_success_by_admin(self):
        """Test that class permission can be provided to staff by admin"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)
        class_ = create_class(institute)
        staff = create_teacher()
        create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
        accept_invite(institute, staff, models.InstituteRole.STAFF)

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': str(staff), 'class_slug': class_.class_slug}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], ' ')
        self.assertEqual(res.data['email'], str(staff))
        self.assertIn('created_on', res.data)
        self.assertIn('profile_pic', res.data)
        self.assertEqual(res.data['inviter_name'], ' ')
        self.assertEqual(res.data['inviter_email'], str(self.user))
        self.assertTrue(models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=staff).exists())

    def test_provide_class_permission_to_admin_success_by_admin(self):
        """Test that class permission can be provided to admin by admin"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)
        class_ = create_class(institute)
        staff = create_teacher()
        create_invite(institute, self.user, staff, models.InstituteRole.ADMIN)
        accept_invite(institute, staff, models.InstituteRole.ADMIN)

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': str(staff), 'class_slug': class_.class_slug}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], ' ')
        self.assertEqual(res.data['email'], str(staff))
        self.assertIn('created_on', res.data)
        self.assertIn('profile_pic', res.data)
        self.assertEqual(res.data['inviter_name'], ' ')
        self.assertEqual(res.data['inviter_email'], str(self.user))
        self.assertTrue(models.InstituteClassPermission.objects.filter(
            to=class_,
            invitee=staff).exists())

    def test_provide_class_permission_to_non_user_fails_by_admin(self):
        """Test that class permission can not be provided to non permitted user."""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)
        class_ = create_class(institute)
        user = create_teacher()

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': str(user), 'class_slug': class_.class_slug}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'User is not a member of this institute.')

    def test_provide_class_permission_to_false_email_fails_by_admin(self):
        """Test that class permission can be provided to invalid user"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)
        class_ = create_class(institute)

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': 'abc@gmail.com', 'class_slug': class_.class_slug}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'This user does not exist.')

    def test_provide_class_permission_to_false_class_fails_by_admin(self):
        """Test that class permission can be provided to staff"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': 'abc@gmail.com', 'class_slug': 'sggdsgs-sdgsg-sgsg'}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Class not found.')

    def test_provide_class_permission_to_admin_fails_by_staff(self):
        """Test that class permission can not be provided by staff"""
        admin = create_teacher('teacher@gamil.com', 'sdfEgafjjjjs')
        institute = create_institute(admin)
        lic = create_institute_license(institute, self.payload)
        create_order(lic, institute)
        class_ = create_class(institute)
        staff = create_teacher()
        create_invite(institute, admin, staff, models.InstituteRole.ADMIN)
        accept_invite(institute, staff, models.InstituteRole.ADMIN)
        create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
        accept_invite(institute, self.user, models.InstituteRole.STAFF)

        res = self.client.post(
            INSTITUTE_ADD_CLASS_PERMISSION,
            {'invitee': str(staff), 'class_slug': class_.class_slug}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Permission denied.')
