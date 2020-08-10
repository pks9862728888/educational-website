import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core import models


INSTITUTE_ADD_CLASS_PERMISSION = reverse('institute:add-class-permission')
INSTITUTE_ADD_SUBJECT_PERMISSION = reverse('institute:add-subject-permission')
INSTITUTE_ADD_SECTION_PERMISSION = reverse('institute:add-section-permission')


def get_institute_create_class_url(institute_slug):
    return reverse("institute:create-class",
                   kwargs={'institute_slug': institute_slug})


def get_institute_list_class_url(institute_slug):
    return reverse("institute:list-all-class",
                   kwargs={'institute_slug': institute_slug})


def get_institute_delete_class_url(class_slug):
    return reverse("institute:delete-class",
                   kwargs={'class_slug': class_slug})


def get_institute_class_permission_list_url(class_slug):
    return reverse("institute:list-class-incharges",
                   kwargs={'class_slug': class_slug})


def get_check_institute_class_permission_url(class_slug):
    return reverse("institute:has-class-perm",
                   kwargs={'class_slug': class_slug})


def get_institute_subject_list_url(class_slug):
    return reverse("institute:list-all-subject",
                   kwargs={'class_slug': class_slug})


def get_institute_section_list_url(class_slug):
    return reverse("institute:list-all-section",
                   kwargs={'class_slug': class_slug})


def create_subject_url(class_slug):
    return reverse("institute:create-subject",
                   kwargs={'class_slug': class_slug})


def create_section_url(class_slug):
    return reverse("institute:create-section",
                   kwargs={'class_slug': class_slug})


def get_institute_subject_permission_list_url(subject_slug):
    return reverse("institute:list-subject-instructors",
                   kwargs={'subject_slug': subject_slug})


def get_institute_section_permission_list_url(section_slug):
    return reverse("institute:list-section-incharges",
                   kwargs={'section_slug': section_slug})


def get_subject_create_course_url(subject_slug):
    return reverse("institute:upload-subject-course-content",
                   kwargs={'subject_slug': subject_slug})


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


def create_subject(class_, name='temp subject', type_=models.InstituteSubjectType.MANDATORY):
    """Creates and returns subject"""
    return models.InstituteSubject.objects.create(
        subject_class=class_,
        name=name,
        type=type_
    )


def create_section(class_, name='temp subject'):
    """Creates and returns section"""
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


def create_institute_class_permission(inviter, invitee, class_):
    """Creates and returns institute class permission"""
    return models.InstituteClassPermission.objects.create(
        inviter=inviter,
        invitee=invitee,
        to=class_
    )


def create_institute_subject_permission(inviter, invitee, subject):
    """Creates and returns institute subject permission"""
    return models.InstituteSubjectPermission.objects.create(
        inviter=inviter,
        invitee=invitee,
        to=subject
    )


def create_institute_section_permission(inviter, invitee, class_):
    """Creates and returns institute subject permission"""
    return models.InstituteSectionPermission.objects.create(
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
    #     self.assertTrue(res.data[0]['has_class_perm'])
    #     self.assertIn('class_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['class_incharges']), 0)
    #
    # def test_get_all_class_by_member_faculty(self):
    #     """Test list all class success by member faculty"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     incharge = create_teacher('incharge@gmail.com', 'indhdfhshhs')
    #     create_institute_class_permission(admin, incharge, class_)
    #
    #     res = self.client.get(
    #         get_institute_list_class_url(institute.institute_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], class_.name)
    #     self.assertEqual(res.data[0]['class_slug'], class_.class_slug)
    #     self.assertFalse(res.data[0]['has_class_perm'])
    #     self.assertIn('class_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['class_incharges']), 1)
    #     self.assertEqual(res.data[0]['class_incharges'][0]['id'], incharge.id)
    #     self.assertEqual(res.data[0]['class_incharges'][0]['email'], str(incharge))
    #     self.assertEqual(res.data[0]['class_incharges'][0]['name'], ' ')
    #
    # def test_get_all_class_by_permitted_faculty(self):
    #     """Test list all class success by member faculty"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_class_permission(admin, self.user, class_)
    #     create_institute_class_permission(admin, admin, class_)
    #     res = self.client.get(
    #         get_institute_list_class_url(institute.institute_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], class_.name)
    #     self.assertEqual(res.data[0]['class_slug'], class_.class_slug)
    #     self.assertTrue(res.data[0]['has_class_perm'])
    #     self.assertIn('class_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['class_incharges']), 2)
    #     self.assertEqual(res.data[0]['class_incharges'][0]['id'], self.user.pk)
    #     self.assertEqual(res.data[0]['class_incharges'][1]['id'], admin.pk)
    #
    # def test_get_all_class_fails_by_non_member_user(self):
    #     """Test list all class fails by non member user"""
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
    #
    # def test_provide_class_permission_to_staff_success_by_admin(self):
    #     """Test that class permission can be provided to staff by admin"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': str(staff), 'class_slug': class_.class_slug}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertIn('created_on', res.data)
    #     self.assertIn('profile_pic', res.data)
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertTrue(models.InstituteClassPermission.objects.filter(
    #         to=class_,
    #         invitee=staff).exists())
    #
    # def test_provide_class_permission_to_admin_success_by_admin(self):
    #     """Test that class permission can be provided to admin by admin"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.ADMIN)
    #     accept_invite(institute, staff, models.InstituteRole.ADMIN)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': str(staff), 'class_slug': class_.class_slug}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertIn('created_on', res.data)
    #     self.assertIn('profile_pic', res.data)
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertTrue(models.InstituteClassPermission.objects.filter(
    #         to=class_,
    #         invitee=staff).exists())
    #
    # def test_provide_class_permission_to_non_user_fails_by_admin(self):
    #     """Test that class permission can not be provided to non permitted user."""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     user = create_teacher()
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': str(user), 'class_slug': class_.class_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'User is not a member of this institute.')
    #
    # def test_provide_class_permission_to_false_email_fails_by_admin(self):
    #     """Test that class permission can be provided to invalid user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': 'abc@gmail.com', 'class_slug': class_.class_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This user does not exist.')
    #
    # def test_provide_class_permission_to_false_class_fails_by_admin(self):
    #     """Test that class permission can be provided to staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': 'abc@gmail.com', 'class_slug': 'sggdsgs-sdgsg-sgsg'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Class not found.')
    #
    # def test_provide_class_permission_to_admin_fails_by_staff(self):
    #     """Test that class permission can not be provided by staff"""
    #     admin = create_teacher('teacher@gamil.com', 'sdfEgafjjjjs')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     create_invite(institute, admin, staff, models.InstituteRole.ADMIN)
    #     accept_invite(institute, staff, models.InstituteRole.ADMIN)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_CLASS_PERMISSION,
    #         {'invitee': str(staff), 'class_slug': class_.class_slug}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_get_all_class_permission_list_successful_no_user_admin(self):
    #     """Test that all permitted class user list successful"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_institute_class_permission_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_get_all_class_permission_list_successful_admin(self):
    #     """Test that admin can get list of all permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     prof = models.UserProfile.objects.filter(user=staff).first()
    #     prof.first_name = 'abc'
    #     prof.last_name = 'aaa'
    #     prof.save()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_institute_class_permission(self.user, staff, class_)
    #
    #     res = self.client.get(
    #         get_institute_class_permission_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], 'abc aaa'.upper())
    #     self.assertEqual(res.data[0]['email'], str(staff))
    #     self.assertEqual(res.data[0]['inviter_name'], ' ')
    #     self.assertEqual(res.data[0]['inviter_email'], str(self.user))
    #     self.assertEqual(res.data[0]['image'], None)
    #     self.assertIn('created_on', res.data[0])
    #
    # def test_get_all_class_permission_list_successful_staff(self):
    #     """Test that staff can get list of all permitted user"""
    #     admin = create_teacher('admin@gmail.com', 'adminglsjdf')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     inviter = create_teacher('inviter@gmail.com', 'asdfsggsgs')
    #     create_invite(institute, admin, inviter, models.InstituteRole.ADMIN)
    #     accept_invite(institute, inviter, models.InstituteRole.ADMIN)
    #     create_invite(institute, inviter, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_invite(institute, inviter, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(inviter, staff, class_)
    #     inviter.delete()
    #
    #     res = self.client.get(
    #         get_institute_class_permission_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], ' ')
    #     self.assertEqual(res.data[0]['email'], str(staff))
    #     self.assertEqual(res.data[0]['inviter_name'], ' ')
    #     self.assertEqual(res.data[0]['inviter_email'], 'Anonymous')
    #     self.assertEqual(res.data[0]['image'], None)
    #     self.assertIn('created_on', res.data[0])
    #
    # def test_get_all_class_permission_list_successful_faculty(self):
    #     """Test that faculty can get list of all permitted user"""
    #     admin = create_teacher('admin@gmail.com', 'adminglsjdf')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     create_invite(institute, admin, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_class_permission(admin, staff, class_)
    #
    #     res = self.client.get(
    #         get_institute_class_permission_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], ' ')
    #     self.assertEqual(res.data[0]['email'], str(staff))
    #     self.assertEqual(res.data[0]['inviter_name'], ' ')
    #     self.assertEqual(res.data[0]['inviter_email'], str(admin))
    #     self.assertEqual(res.data[0]['image'], None)
    #     self.assertIn('created_on', res.data[0])
    #
    # def test_get_all_class_permission_list_fails_non_user(self):
    #     """Test that non user can not get list of all permitted user"""
    #     admin = create_teacher('admin@gmail.com', 'adminglsjdf')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     staff = create_teacher()
    #     create_invite(institute, admin, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, staff, class_)
    #
    #     res = self.client.get(
    #         get_institute_class_permission_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_check_class_perm_successful_admin(self):
    #     """Test admin class perm successful"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_check_institute_class_permission_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], True)
    #
    # def test_check_class_perm_successful_non_permitted_user(self):
    #     """Test non permitted user class perm false"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.get(
    #         get_check_institute_class_permission_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], False)
    #
    # def test_check_class_perm_fails_non_institute_member_user(self):
    #     """Test non permitted user class perm false"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_check_institute_class_permission_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_check_class_perm_successful_staff(self):
    #     """Test staff class perm successful"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.get(
    #         get_check_institute_class_permission_url(class_.class_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['status'], True)
    #
    # def test_subject_creation_by_admin_success(self):
    #     """Test that admin can create subject"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], 'subject')
    #     self.assertEqual(res.data['type'], models.InstituteSubjectType.MANDATORY)
    #     self.assertIn('created_on', res.data)
    #
    # def test_subject_creation_by_authorized_staff_success(self):
    #     """Test that staff can create subject"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], 'subject')
    #     self.assertEqual(res.data['type'], models.InstituteSubjectType.MANDATORY)
    #     self.assertIn('created_on', res.data)
    #
    # def test_subject_creation_by_unauthorized_staff_fails(self):
    #     """Test that unauthorized staff can not create subject"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_subject_creation_by_non_user(self):
    #     """Test that non permitted user can not create subject"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_duplicate_subject_creation_fails(self):
    #     """Test that duplicate subject can not be created"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #     res = self.client.post(
    #         create_subject_url(class_.class_slug),
    #         {'name': 'Subject', 'type': models.InstituteSubjectType.MANDATORY}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Subject with same name exists.')
    #
    # def test_section_creation_by_admin_success(self):
    #     """Test that admin can create section"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'A'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], 'a')
    #     self.assertIn('created_on', res.data)
    #     self.assertIn('section_slug', res.data)
    #     self.assertTrue(len('section_slug') > 0)
    #
    # def test_section_creation_by_authorized_staff_success(self):
    #     """Test that staff can create section"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'Section 2'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], 'section 2')
    #     self.assertIn('created_on', res.data)
    #     self.assertIn('section_slug', res.data)
    #     self.assertTrue(len('section_slug') > 0)
    #
    # def test_section_creation_by_unauthorized_staff_fails(self):
    #     """Test that unauthorized staff can not create section"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'Subject'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_section_creation_by_non_user(self):
    #     """Test that non permitted user can not create section"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'section'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_duplicate_section_creation_fails(self):
    #     """Test that duplicate section can not be created"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #
    #     self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'Subject'}
    #     )
    #     res = self.client.post(
    #         create_section_url(class_.class_slug),
    #         {'name': 'Subject'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Section with same name exists.')
    #
    # def test_add_subject_permission_to_staff_success_by_admin(self):
    #     """Test that admin can add subject permission to staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_subject_permission_to_staff_success_by_permitted_staff(self):
    #     """Test that permitted staff can add subject permission to staff"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #     create_invite(institute, admin, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_subject_permission_to_faculty_success_by_admin(self):
    #     """Test that admin can add subject permission to faculty"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, self.user, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(faculty), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(faculty))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_subject_permission_to_faculty_success_by_permitted_staff(self):
    #     """Test that permitted staff can add subject permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(faculty), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(faculty))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_subject_permission_to_faculty_fails_by_non_permitted_staff(self):
    #     """Test that unpermitted staff can not add subject permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(faculty), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_subject_permission_to_faculty_fails_by_non_member(self):
    #     """Test that non member can not add subject permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(faculty), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_subject_permission_to_staff_twice_fails_by_admin(self):
    #     """Test that staff permission can not be added twice"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': sub.subject_slug}
    #     )
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'User is already an instructor.')
    #
    # def test_add_subject_permission_to_invalid_staff_fails(self):
    #     """Test that staff permission can not be added to invalid staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': 'adf@gd.cpm', 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This user does not exist.')
    #
    # def test_add_subject_permission_to_non_member_fails(self):
    #     """Test that staff permission can not be added to non member staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': sub.subject_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'User is not a member of this institute.')
    #
    # def test_add_subject_permission_to_wrong_subject_fails(self):
    #     """Test that staff permission can not be added to invalid subject"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SUBJECT_PERMISSION,
    #         {'invitee': str(staff), 'subject_slug': 'adf'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Subject not found.')
    #
    # def test_add_section_permission_to_staff_success_by_admin(self):
    #     """Test that admin can add subject permission to staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_section_permission_to_staff_success_by_permitted_staff(self):
    #     """Test that permitted staff can add section permission to staff"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #     create_invite(institute, admin, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(staff))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_section_permission_to_faculty_success_by_admin(self):
    #     """Test that admin can add section permission to faculty"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, self.user, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(faculty), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(faculty))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_section_permission_to_faculty_success_by_permitted_staff(self):
    #     """Test that permitted staff can add section permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(faculty), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], ' ')
    #     self.assertEqual(res.data['email'], str(faculty))
    #     self.assertEqual(res.data['inviter_name'], ' ')
    #     self.assertEqual(res.data['inviter_email'], str(self.user))
    #     self.assertEqual(res.data['image'], None)
    #     self.assertIn('created_on', res.data)
    #
    # def test_add_section_permission_to_faculty_fails_by_non_permitted_staff(self):
    #     """Test that unpermitted staff can not add section permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(faculty), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_section_permission_to_faculty_fails_by_non_member(self):
    #     """Test that non member can not add section permission to faculty"""
    #     admin = create_teacher('adminer@gmail.com', 'adminguersjnej')
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     faculty = create_teacher()
    #     create_invite(institute, admin, faculty, models.InstituteRole.FACULTY)
    #     accept_invite(institute, faculty, models.InstituteRole.FACULTY)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(faculty), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_section_permission_to_staff_twice_fails_by_admin(self):
    #     """Test that staff permission can not be added twice"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': sec.section_slug}
    #     )
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'User already has section permission.')
    #
    # def test_add_section_permission_to_invalid_staff_fails(self):
    #     """Test that section permission can not be added to invalid staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': 'adf@gd.cpm', 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This user does not exist.')
    #
    # def test_add_section_permission_to_non_member_fails(self):
    #     """Test that staff permission can not be added to non member staff"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': sec.section_slug}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'User is not a member of this institute.')
    #
    # def test_add_section_permission_to_wrong_subject_fails(self):
    #     """Test that staff permission can not be added to invalid section"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     create_order(lic, institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     staff = create_teacher()
    #     create_invite(institute, self.user, staff, models.InstituteRole.STAFF)
    #     accept_invite(institute, staff, models.InstituteRole.STAFF)
    #
    #     res = self.client.post(
    #         INSTITUTE_ADD_SECTION_PERMISSION,
    #         {'invitee': str(staff), 'section_slug': 'adf'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Section not found.')
    #
    # def test_list_all_subject_with_no_created_subject_success(self):
    #     """Test that listing subject success when no subjects are created"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_list_all_subject_by_admin_success_with_created_subject(self):
    #     """Test that listing subject success when subjects are created"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sub.name)
    #     self.assertEqual(res.data[0]['id'], sub.id)
    #     self.assertEqual(res.data[0]['type'], sub.type)
    #     self.assertEqual(res.data[0]['subject_slug'], sub.subject_slug)
    #     self.assertIn('created_on', res.data[0])
    #     self.assertTrue(res.data[0]['has_subject_perm'])
    #     self.assertIn('subject_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['subject_incharges']), 0)
    #
    # def test_list_all_subject_by_member_staff_success(self):
    #     """Test that listing subject success when subjects are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     incharge = create_teacher('incharge@gmail.com', 'inchargeusername')
    #     create_institute_subject_permission(admin, incharge, sub)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sub.name)
    #     self.assertEqual(res.data[0]['type'], sub.type)
    #     self.assertEqual(res.data[0]['subject_slug'], sub.subject_slug)
    #     self.assertFalse(res.data[0]['has_subject_perm'])
    #     self.assertIn('subject_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['subject_incharges']), 1)
    #     self.assertEqual(res.data[0]['subject_incharges'][0]['id'], incharge.pk)
    #     self.assertEqual(res.data[0]['subject_incharges'][0]['email'], str(incharge))
    #     self.assertEqual(res.data[0]['subject_incharges'][0]['name'], ' ')
    #
    # def test_list_all_subject_by_permitted_faculty_success(self):
    #     """Test that listing subject success when subjects are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_subject_permission(admin, self.user, sub)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sub.name)
    #     self.assertEqual(res.data[0]['type'], sub.type)
    #     self.assertEqual(res.data[0]['subject_slug'], sub.subject_slug)
    #     self.assertTrue(res.data[0]['has_subject_perm'])
    #     self.assertIn('subject_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['subject_incharges']), 1)
    #
    # def test_list_all_subject_by_non_member_user_fails(self):
    #     """Test that listing subject fails by non member user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sub = create_subject(class_)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_all_subject_by_invited_member_staff_fails(self):
    #     """Test that listing subject success when subjects are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     create_subject(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.get(
    #         get_institute_subject_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_all_section_with_no_created_section_success(self):
    #     """Test that listing subject success when no sections are created"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_list_all_section_by_admin_success_with_created_section(self):
    #     """Test that listing section success when section are created"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     incharge = create_teacher()
    #     create_institute_section_permission(self.user, incharge, sec)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sec.name)
    #     self.assertEqual(res.data[0]['section_slug'], sec.section_slug)
    #     self.assertTrue(res.data[0]['has_section_perm'])
    #     self.assertIn('section_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['section_incharges']), 1)
    #     self.assertEqual(res.data[0]['section_incharges'][0]['id'], incharge.pk)
    #     self.assertEqual(res.data[0]['section_incharges'][0]['email'], str(incharge))
    #     self.assertEqual(res.data[0]['section_incharges'][0]['name'], ' ')
    #
    # def test_list_all_section_by_member_staff_success(self):
    #     """Test that listing section success when sections are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sec.name)
    #     self.assertEqual(res.data[0]['id'], sec.id)
    #     self.assertEqual(res.data[0]['section_slug'], sec.section_slug)
    #     self.assertFalse(res.data[0]['has_section_perm'])
    #     self.assertIn('created_on', res.data[0])
    #     self.assertIn('section_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['section_incharges']), 0)
    #
    # def test_list_all_section_by_permitted_faculty_success(self):
    #     """Test that listing section success when section are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     sec = create_section(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_section_permission(admin, self.user, sec)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], sec.name)
    #     self.assertEqual(res.data[0]['section_slug'], sec.section_slug)
    #     self.assertTrue(res.data[0]['has_section_perm'])
    #     self.assertIn('section_incharges', res.data[0])
    #     self.assertEqual(len(res.data[0]['section_incharges']), 1)
    #
    # def test_list_all_section_by_non_member_user_fails(self):
    #     """Test that listing section fails by non member user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     create_section(class_)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_all_section_by_invited_member_staff_fails(self):
    #     """Test that listing section success when sections are created"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     class_ = create_class(institute)
    #     create_section(class_)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.get(
    #         get_institute_section_list_url(class_.class_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_subject_permission_success_no_permitted_user(self):
    #     """Test that subject permission list success with no permitted user"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     subject = create_subject(create_class(institute))
    #
    #     res = self.client.get(
    #         get_institute_subject_permission_list_url(subject.subject_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_list_subject_permission_success_admin(self):
    #     """Test that subject permission list success"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     sub = create_subject(create_class(institute))
    #     teacher = create_teacher()
    #     perm = create_institute_subject_permission(self.user, teacher, sub)
    #
    #     res = self.client.get(
    #         get_institute_subject_permission_list_url(sub.subject_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['id'], perm.id)
    #     self.assertEqual(res.data[0]['name'], ' ')
    #     self.assertEqual(res.data[0]['email'], str(teacher))
    #     self.assertEqual(res.data[0]['inviter_name'], ' ')
    #     self.assertEqual(res.data[0]['inviter_email'], str(self.user))
    #     self.assertIn('created_on', res.data[0])
    #
    # def test_list_subject_permission_fails_non_user(self):
    #     """Test that subject permission list fails for non institute member"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     sub = create_subject(create_class(institute))
    #
    #     res = self.client.get(
    #         get_institute_subject_permission_list_url(sub.subject_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_section_permission_success_no_permitted_user(self):
    #     """Test that subject permission list success with no permitted user"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     section = create_section(create_class(institute))
    #
    #     res = self.client.get(
    #         get_institute_section_permission_list_url(section.section_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 0)
    #
    # def test_list_section_permission_success_admin(self):
    #     """Test that section permission list success"""
    #     institute = create_institute(self.user)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     section = create_section(create_class(institute))
    #     teacher = create_teacher()
    #     perm = create_institute_section_permission(self.user, teacher, section)
    #
    #     res = self.client.get(
    #         get_institute_section_permission_list_url(section.section_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['id'], perm.id)
    #     self.assertEqual(res.data[0]['name'], ' ')
    #     self.assertEqual(res.data[0]['email'], str(teacher))
    #     self.assertEqual(res.data[0]['inviter_name'], ' ')
    #     self.assertEqual(res.data[0]['inviter_email'], str(self.user))
    #     self.assertEqual(res.data[0]['image'], None)
    #     self.assertIn('created_on', res.data[0])
    #
    # def test_list_section_permission_fails_non_user(self):
    #     """Test that section permission list fails for non institute member"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     create_order(create_institute_license(institute, self.payload), institute)
    #     section = create_section(create_class(institute))
    #
    #     res = self.client.get(
    #         get_institute_section_permission_list_url(section.section_slug)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')

    def test_upload_meet_your_instructor_link_success_by_permitted_user(self):
        """Test that permitted user can upload link content"""
        institute = create_institute(self.user)
        order = create_order(create_institute_license(institute, self.payload), institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        subject = create_subject(create_class(institute))
        create_institute_subject_permission(self.user, self.user, subject)

        payload = {
            'subject': subject.subject_slug,
            'order': 1,
            'title': 'temp title',
            'file_type': models.StudyMaterialContentType.EXTERNAL_LINK,
            'url': 'https://www.google.com/',
            'target_date': '2000-12-12',
            'model': 'MI',
            'size': '0.01'
        }

        res = self.client.post(
            get_subject_create_course_url(subject.subject_slug),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['order'], payload['order'])
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['file_type'], payload['file_type'])
        self.assertEqual(res.data['url'], payload['url'])
        self.assertEqual(res.data['target_date'], payload['target_date'])
        self.assertIn('uploaded_on', res.data)
        self.assertNotIn('file', res.data)

    def test_upload_meet_your_instructor_link_success_without_target_date(self):
        """Test that permitted user can upload link content"""
        institute = create_institute(self.user)
        order = create_order(create_institute_license(institute, self.payload), institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        subject = create_subject(create_class(institute))
        create_institute_subject_permission(self.user, self.user, subject)

        payload = {
            'subject': subject.subject_slug,
            'order': 1,
            'title': 'temp title',
            'file_type': models.StudyMaterialContentType.EXTERNAL_LINK,
            'url': 'https://www.google.com/',
            'model': 'MI'
        }

        res = self.client.post(
            get_subject_create_course_url(subject.subject_slug),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['order'], payload['order'])
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(res.data['file_type'], payload['file_type'])
        self.assertEqual(res.data['url'], payload['url'])
        self.assertIn('uploaded_on', res.data)
        self.assertNotIn('file', res.data)
        self.assertEqual(res.data['target_date'], None)

    def test_upload_meet_your_instructor_link_fails_by_unpermitted_user(self):
        """Test that unpermitted user can not upload link content"""
        institute = create_institute(self.user)
        order = create_order(create_institute_license(institute, self.payload), institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        subject = create_subject(create_class(institute))

        payload = {
            'subject': subject.subject_slug,
            'order': 1,
            'title': 'temp title',
            'file_type': models.StudyMaterialContentType.EXTERNAL_LINK,
            'url': 'https://www.google.com/',
            'target_date': '2000-12-12',
            'model': 'MI'
        }

        res = self.client.post(
            get_subject_create_course_url(subject.subject_slug),
            payload
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Permission denied.')
