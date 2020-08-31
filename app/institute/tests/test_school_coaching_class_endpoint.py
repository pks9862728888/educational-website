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


def get_add_student_to_institute_url(institute_slug):
    return reverse("institute:add-student-to-institute",
                   kwargs={'institute_slug': institute_slug})


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
    return reverse("institute:add-subject-course-content",
                   kwargs={'subject_slug': subject_slug})


def get_subject_course_content_min_statistics_url(subject_slug):
    return reverse("institute:subject-course-content-min-statistics",
                   kwargs={'subject_slug': subject_slug})


def get_subject_course_content_for_specific_view_url(subject_slug, view):
    return reverse("institute:list-subject-specific-view-course-contents",
                   kwargs={'subject_slug': subject_slug, 'view': view})


def edit_institute_study_material_url(subject_slug, pk_):
    return reverse("institute:edit-subject-course-content",
                   kwargs={'subject_slug': subject_slug, 'pk': pk_})


def get_study_material_delete_url(pk):
    return reverse("institute:delete-subject-course-content",
                   kwargs={'pk': pk})


def get_week_add_url(subject_slug):
    return reverse("institute:add-week",
                   kwargs={'subject_slug': subject_slug})


def get_add_subject_view_url(subject_slug):
    return reverse("institute:add-view",
                   kwargs={'subject_slug': subject_slug})


def get_delete_week_url(institute_slug, subject_slug, view_key, week_value):
    return reverse("institute:delete-week",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'view_key': view_key,
                           'week_value': week_value})


def get_delete_view_url(institute_slug, subject_slug, view_key):
    return reverse("institute:delete-subject-view",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'view_key': view_key})


def get_edit_subject_module_url(subject_slug, view_key):
    return reverse("institute:edit-subject-view-name",
                   kwargs={'subject_slug': subject_slug,
                           'view_key': view_key})


def get_course_preview_min_details(institute_slug, subject_slug):
    return reverse("institute:subject-course-preview-min-details",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug})


def get_institute_subject_content_ask_question_url(institute_slug, subject_slug, pk):
    return reverse("institute:ask-new-question",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'course_content_id': pk})


def get_answer_question_url(institute_slug, subject_slug, pk):
    return reverse("institute:answer-question",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'question_pk': pk})


def get_upvote_downvote_question_url(institute_slug, subject_slug, question_pk):
    return reverse("institute:upvote-downvote-question",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'question_pk': question_pk})


def get_upvote_downvote_answer_url(institute_slug, subject_slug, answer_pk):
    return reverse("institute:upvote-downvote-answer",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'answer_pk': answer_pk})


def get_delete_question_url(question_pk):
    return reverse("institute:delete-question",
                   kwargs={'question_pk': question_pk})


def get_delete_answer_url(subject_slug, answer_pk):
    return reverse("institute:delete-answer",
                   kwargs={'subject_slug': subject_slug,
                           'answer_pk': answer_pk})


def get_pin_answer_url(answer_pk):
    return reverse("institute:pin-answer",
                   kwargs={'answer_pk': answer_pk})


def get_answer_list_url(institute_slug, subject_slug, question_pk):
    return reverse("institute:list-answers",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'question_pk': question_pk})


def get_question_list_url(institute_slug, subject_slug, course_content_pk):
    return reverse("institute:list-questions",
                   kwargs={'institute_slug': institute_slug,
                           'subject_slug': subject_slug,
                           'course_content_pk': course_content_pk})


def get_classes_key_value_url(institute_slug):
    return reverse("institute:get-class-slug-name-pairs",
                   kwargs={'institute_slug': institute_slug})


def create_teacher(email='abc@gmail.com', username='tempusername'):
    """Creates and return teacher"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tempupassword',
        is_teacher=True
    )


def create_student(email='studesdfnt@gmail.com', username='studentusername'):
    """Creates and return student"""
    return get_user_model().objects.create_user(
        email=email,
        username=username,
        password='tammslkjdpasswoers',
        is_student=True
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


def create_subject_course_content(
        subject, order, url="www.google.com", title="Temp tile",
        content_type=models.StudyMaterialContentType.EXTERNAL_LINK,
        target_date='2000-12-12', view=models.StudyMaterialView.MEET_YOUR_INSTRUCTOR):
    """Create and return subject course content"""
    content = models.InstituteSubjectCourseContent.objects.create(
        course_content_subject=subject,
        order=order,
        title=title,
        content_type=content_type,
        view=view,
        target_date=target_date
    )

    models.SubjectExternalLinkStudyMaterial.objects.create(
        external_link_study_material=content,
        url=url
    )
    return content


def ask_question(course_content, user, anonymous=True, question='a', description='a', rgb_color='#ffffff'):
    """Creates and asks a new question"""
    return models.InstituteSubjectCourseContentQuestions.objects.create(
        course_content=course_content,
        user=user,
        anonymous=anonymous,
        question=question,
        description=description,
        rgb_color=rgb_color
    )


def answer_question(question, user, answer='a', anonymous=True, rgb_color='#ffffff'):
    """Creates and returns answer"""
    return models.InstituteSubjectCourseContentAnswer.objects.create(
        content_question=question,
        user=user,
        anonymous=anonymous,
        answer=answer,
        rgb_color=rgb_color
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
    #
    # def test_upload_meet_your_instructor_link_success_by_permitted_user(self):
    #     """Test that permitted user can upload link content"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     subject = create_subject(create_class(institute))
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     payload = {
    #         'subject': subject.subject_slug,
    #         'title': 'temp title',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'target_date': '2000-12-12',
    #         'view': models.StudyMaterialView.MEET_YOUR_INSTRUCTOR,
    #         'url': 'https://www.google.com/'
    #     }
    #
    #     res = self.client.post(
    #         get_subject_create_course_url(subject.subject_slug),
    #         payload, format='json'
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['title'], payload['title'])
    #     self.assertEqual(res.data['content_type'], payload['content_type'])
    #     self.assertEqual(res.data['target_date'], payload['target_date'])
    #     self.assertIn('uploaded_on', res.data)
    #     self.assertIn('order', res.data)
    #     self.assertEqual(res.data['data']['url'], payload['url'])
    #     self.assertNotIn('file', res.data)
    #     stats = models.InstituteSubjectStatistics.objects.filter(
    #         statistics_subject=subject
    #     ).first()
    #     self.assertEqual(stats.max_order, 1)
    #     self.assertEqual(stats.storage, 0.0)
    #
    # def test_upload_meet_your_instructor_link_success_without_target_date(self):
    #     """Test that permitted user can upload link content"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     subject = create_subject(create_class(institute))
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     payload = {
    #         'subject': subject.subject_slug,
    #         'title': 'temp title',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'view': models.StudyMaterialView.MEET_YOUR_INSTRUCTOR,
    #         'url': 'https://www.google.com/',
    #     }
    #
    #     res = self.client.post(
    #         get_subject_create_course_url(subject.subject_slug),
    #         payload, format='json'
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['title'], payload['title'])
    #     self.assertEqual(res.data['content_type'], payload['content_type'])
    #     self.assertIn('uploaded_on', res.data)
    #     self.assertIn('order', res.data)
    #     self.assertEqual(res.data['data']['url'], payload['url'])
    #     self.assertNotIn('file', res.data)
    #     stats = models.InstituteSubjectStatistics.objects.filter(
    #         statistics_subject=subject
    #     ).first()
    #     self.assertEqual(stats.max_order, 1)
    #     self.assertEqual(stats.storage, 0.0)
    #
    # def test_upload_meet_your_instructor_link_fails_by_unpermitted_user(self):
    #     """Test that unpermitted user can not upload link content"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     subject = create_subject(create_class(institute))
    #
    #     payload = {
    #         'subject': subject.subject_slug,
    #         'title': 'temp title',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'target_date': '2000-12-12',
    #         'view': models.StudyMaterialView.MEET_YOUR_INSTRUCTOR,
    #         'url': 'https://www.google.com/',
    #         'size': '0.01',
    #     }
    #
    #     res = self.client.post(
    #         get_subject_create_course_url(subject.subject_slug),
    #         payload)
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_all_subject_min_statistics_success_by_admin(self):
    #     """Test that listing all subject min statistics success by admin"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #
    #     res = self.client.get(
    #         get_subject_course_content_min_statistics_url(subject.subject_slug))
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data[models.StudyMaterialView.MEET_YOUR_INSTRUCTOR], 1)
    #     self.assertEqual(res.data[models.StudyMaterialView.COURSE_OVERVIEW], 0)
    #     self.assertEqual(res.data['storage_used'], 0.0)
    #     self.assertEqual(res.data['total_storage'], 100.0)
    #
    # def test_list_all_subject_min_statistics_success_by_faculty(self):
    #     """Test that listing all subject min statistics success by admin"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #     create_institute_subject_permission(admin, self.user, subject)
    #
    #     res = self.client.get(
    #         get_subject_course_content_min_statistics_url(subject.subject_slug))
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data[models.StudyMaterialView.MEET_YOUR_INSTRUCTOR], 1)
    #     self.assertEqual(res.data[models.StudyMaterialView.COURSE_OVERVIEW], 0)
    #     self.assertEqual(res.data['storage_used'], 0.0)
    #     self.assertEqual(res.data['total_storage'], 100.0)
    #
    # def test_list_all_subject_min_statistics_fails_by_non_permitted_user(self):
    #     """Test that listing all subject min statistics fails"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #
    #     res = self.client.get(
    #         get_subject_course_content_min_statistics_url(subject.subject_slug))
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_get_subject_materials_for_specific_view_success_by_admin(self):
    #     """Test that study materials for specific view success by admin"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #
    #     res = self.client.get(
    #         get_subject_course_content_for_specific_view_url(
    #             subject.subject_slug, models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['view'], models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     self.assertEqual(res.data[0]['title'], 'Temp tile')
    #     self.assertEqual(res.data[0]['content_type'], models.StudyMaterialContentType.EXTERNAL_LINK)
    #     self.assertEqual(res.data[0]['target_date'], '2000-12-12')
    #     self.assertEqual(res.data[0]['order'], 21)
    #     self.assertEqual(res.data[0]['data']['url'], 'www.google.com')
    #     self.assertIn('id', res.data[0])
    #     self.assertIn('order', res.data[0])
    #     self.assertIn('uploaded_on', res.data[0])
    #
    # def test_get_subject_materials_for_specific_view_success_by_permitted_user(self):
    #     """Test that study materials for specific view success by permitted user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #     create_institute_subject_permission(admin, self.user, subject)
    #
    #     res = self.client.get(
    #         get_subject_course_content_for_specific_view_url(
    #             subject.subject_slug, models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['view'], models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     self.assertEqual(res.data[0]['title'], 'Temp tile')
    #     self.assertEqual(res.data[0]['content_type'], models.StudyMaterialContentType.EXTERNAL_LINK)
    #     self.assertEqual(res.data[0]['target_date'], '2000-12-12')
    #     self.assertEqual(res.data[0]['order'], 21)
    #     self.assertEqual(res.data[0]['data']['url'], 'www.google.com')
    #     self.assertIn('id', res.data[0])
    #     self.assertIn('order', res.data[0])
    #     self.assertIn('uploaded_on', res.data[0])
    #
    # def test_get_subject_materials_for_specific_view_fails_by_unpermitted_user(self):
    #     """Test that study materials for specific view fails by unpermitted user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_subject_course_content(subject, 21)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #     create_institute_class_permission(admin, self.user, class_)
    #
    #     res = self.client.get(
    #         get_subject_course_content_for_specific_view_url(
    #             subject.subject_slug, models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_study_materials_success_by_admin(self):
    #     """Test that admin can delete study materials"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     content = create_subject_course_content(subject, 21)
    #
    #     res = self.client.delete(
    #         get_study_material_delete_url(content.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.InstituteSubjectCourseContent.objects.filter(pk=content.pk).exists())
    #     self.assertFalse(models.SubjectExternalLinkStudyMaterial.objects.filter(
    #         external_link_study_material__pk=content.pk).exists())
    #
    # def test_delete_study_materials_success_by_permitted_user(self):
    #     """Test that permitted faculty can delete study materials"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     content = create_subject_course_content(subject, 21)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_subject_permission(admin, self.user, subject)
    #
    #     res = self.client.delete(
    #         get_study_material_delete_url(content.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.InstituteSubjectCourseContent.objects.filter(pk=content.pk).exists())
    #     self.assertFalse(models.SubjectExternalLinkStudyMaterial.objects.filter(
    #         external_link_study_material__pk=content.pk).exists())
    #
    # def test_delete_study_materials_fails_by_unpermitted_faculty(self):
    #     """Test that non permitted faculty can not delete study materials"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     content = create_subject_course_content(subject, 21)
    #     create_invite(institute, admin, self.user, models.InstituteRole.STAFF)
    #     accept_invite(institute, self.user, models.InstituteRole.STAFF)
    #
    #     res = self.client.delete(
    #         get_study_material_delete_url(content.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #     self.assertTrue(models.InstituteSubjectCourseContent.objects.filter(pk=content.pk).exists())
    #     self.assertTrue(models.SubjectExternalLinkStudyMaterial.objects.filter(
    #         external_link_study_material__pk=content.pk).exists())
    #
    # def test_can_not_delete_twice(self):
    #     """Test that permitted faculty can delete study materials twice"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     content = create_subject_course_content(subject, 21)
    #     create_invite(institute, admin, self.user, models.InstituteRole.FACULTY)
    #     accept_invite(institute, self.user, models.InstituteRole.FACULTY)
    #     create_institute_subject_permission(admin, self.user, subject)
    #
    #     self.client.delete(
    #         get_study_material_delete_url(content.pk)
    #     )
    #     res = self.client.delete(
    #         get_study_material_delete_url(content.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.InstituteSubjectCourseContent.objects.filter(pk=content.pk).exists())
    #     self.assertFalse(models.SubjectExternalLinkStudyMaterial.objects.filter(
    #         external_link_study_material__pk=content.pk).exists())
    #
    # def test_permitted_user_can_edit_existing_study_material_details(self):
    #     """Test that editing study material details is successful"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     subject = create_subject(create_class(institute))
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     study_material = models.InstituteSubjectCourseContent.objects.create(
    #         course_content_subject=subject,
    #         order=1,
    #         title='aaa',
    #         content_type=models.StudyMaterialContentType.EXTERNAL_LINK,
    #         view=models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #     models.SubjectExternalLinkStudyMaterial.objects.create(
    #         external_link_study_material=study_material,
    #         url='a'
    #     )
    #
    #     payload = {
    #         'title': 'bbb',
    #         'description': 'acvd',
    #         'target_date': '2020-12-12',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'data': {
    #             'url': 'a'
    #         }
    #     }
    #
    #     res = self.client.patch(
    #         edit_institute_study_material_url(subject.subject_slug, study_material.pk),
    #         payload,
    #         format='json'
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['data']['url'], payload['data']['url'])
    #     self.assertEqual(res.data['id'], study_material.pk)
    #     self.assertEqual(res.data['order'], study_material.order)
    #     self.assertEqual(res.data['content_type'], study_material.content_type)
    #     self.assertEqual(res.data['view'], study_material.view)
    #     self.assertEqual(res.data['description'], payload['description'])
    #     self.assertEqual(res.data['title'], payload['title'])
    #     self.assertIn('target_date', res.data)
    #     self.assertEqual(res.data['target_date'], payload['target_date'])
    #
    #     material = models.InstituteSubjectCourseContent.objects.filter(pk=study_material.pk).first()
    #     self.assertEqual(material.title, payload['title'])
    #     self.assertEqual(material.description, payload['description'])
    #     self.assertEqual(str(material.target_date), payload['target_date'])
    #
    # def test_permitted_user_can_edit_existing_study_material_details_no_target_date(self):
    #     """Test that editing study material details is successful"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     subject = create_subject(create_class(institute))
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     study_material = models.InstituteSubjectCourseContent.objects.create(
    #         course_content_subject=subject,
    #         order=1,
    #         title='aaa',
    #         content_type=models.StudyMaterialContentType.EXTERNAL_LINK,
    #         view=models.StudyMaterialView.MEET_YOUR_INSTRUCTOR,
    #         target_date='2020-12-12')
    #     models.SubjectExternalLinkStudyMaterial.objects.create(
    #         external_link_study_material=study_material,
    #         url='a'
    #     )
    #
    #     payload = {
    #         'title': 'bbb',
    #         'description': 'decsdf',
    #         'target_date': '',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'data': {
    #             'url': 'b'
    #         }
    #     }
    #
    #     res = self.client.patch(
    #         edit_institute_study_material_url(subject.subject_slug, study_material.pk),
    #         payload,
    #         format='json'
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['id'], study_material.pk)
    #     self.assertEqual(res.data['order'], study_material.order)
    #     self.assertEqual(res.data['content_type'], study_material.content_type)
    #     self.assertEqual(res.data['view'], study_material.view)
    #     self.assertEqual(res.data['description'], payload['description'])
    #     self.assertEqual(res.data['title'], payload['title'])
    #     self.assertNotIn('target_date', res.data)
    #     self.assertEqual(res.data['data']['url'], payload['data']['url'])
    #
    #     material = models.InstituteSubjectCourseContent.objects.filter(pk=study_material.pk).first()
    #     self.assertEqual(material.title, payload['title'])
    #     self.assertEqual(material.description, payload['description'])
    #     self.assertEqual(material.target_date, None)
    #
    # def test_unpermitted_user_can_not_edit_existing_study_material_details(self):
    #     """Test that editing study material details is successful"""
    #     institute = create_institute(self.user)
    #     order = create_order(create_institute_license(institute, self.payload), institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     subject = create_subject(create_class(institute))
    #     study_material = models.InstituteSubjectCourseContent.objects.create(
    #         course_content_subject=subject,
    #         order=1,
    #         title='aaa',
    #         content_type=models.StudyMaterialContentType.EXTERNAL_LINK,
    #         view=models.StudyMaterialView.MEET_YOUR_INSTRUCTOR)
    #
    #     payload = {
    #         'title': 'bbb',
    #         'description': 'aaa',
    #         'target_date': '',
    #         'content_type': models.StudyMaterialContentType.EXTERNAL_LINK,
    #         'data': {
    #             'url': 'b'
    #         }
    #     }
    #
    #     res = self.client.patch(
    #         edit_institute_study_material_url(subject.subject_slug, study_material.pk),
    #         payload,
    #         format='json'
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_week_successful_by_permitted_user(self):
    #     """Test that adding week is successful by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     res = self.client.post(
    #         get_week_add_url(subject.subject_slug),
    #         {'view_key': 'M1'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['week'], 2)
    #
    #     view = models.SubjectViewNames.objects.filter(
    #         view_subject=subject,
    #         key='M1'
    #     ).first()
    #     self.assertEqual(models.SubjectViewWeek.objects.filter(
    #         week_view=view
    #     ).count(), 2)
    #     self.assertTrue(models.SubjectViewWeek.objects.filter(
    #         week_view=view,
    #         value=2
    #     ).exists())
    #
    # def test_add_week_fails_by_unpermitted_user(self):
    #     """Test that adding week is fails by unpermitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #
    #     res = self.client.post(
    #         get_week_add_url(subject.subject_slug),
    #         {'view_key': 'M1'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_view_success(self):
    #     """Test that adding view is success by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     res = self.client.post(
    #         get_add_subject_view_url(subject.subject_slug),
    #         {'name': 'ABC aaa'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['name'], 'ABC aaa')
    #     self.assertEqual(res.data[1], 0)
    #     self.assertEqual(res.data['count'], 0)
    #     self.assertEqual(res.data['weeks'], [1])
    #
    # def test_add_view_fails_for_unpermitted_user(self):
    #     """Test that adding view is fails by unpermitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #
    #     res = self.client.post(
    #         get_add_subject_view_url(subject.subject_slug),
    #         {'name': 'ABC aaa'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_add_view_fails_for_invalid_credentials(self):
    #     """Test that adding view is fails by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     res = self.client.post(
    #         get_add_subject_view_url(subject.subject_slug),
    #         {}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Name is required and can not be blank.')
    #
    # def test_delete_week_successful(self):
    #     """Test that permitted user can delete week"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     res = self.client.delete(
    #         get_delete_week_url(institute.institute_slug, subject.subject_slug, 'MI', 1)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    #     view = models.SubjectViewNames.objects.filter(
    #         view_subject=subject
    #     ).first()
    #     self.assertFalse(models.SubjectViewWeek.objects.filter(
    #         week_view=view,
    #         value=1
    #     ).exists())
    #
    # def test_delete_week_fails_by_unpermitted_user(self):
    #     """Test that unpermitted user can not delete week"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #
    #     res = self.client.delete(
    #         get_delete_week_url(institute.institute_slug, subject.subject_slug, 'MI', 1)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_module_success(self):
    #     """Test that permitted user can delete module"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     view_pk = models.SubjectViewNames.objects.filter(
    #         view_subject=subject,
    #         key='M1'
    #     ).first().pk
    #
    #     res = self.client.delete(
    #         get_delete_view_url(institute.institute_slug, subject.subject_slug, 'M1')
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(models.SubjectViewNames.objects.filter(
    #         view_subject=subject,
    #         key='M1'
    #     ).exists())
    #     self.assertFalse(models.SubjectViewWeek.objects.filter(
    #         week_view__pk=view_pk
    #     ).exists())
    #
    # def test_delete_module_fails_by_unpermitted_user(self):
    #     """Test that unpermitted user can not delete module"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view_pk = models.SubjectViewNames.objects.filter(
    #         view_subject=subject,
    #         key='M1'
    #     ).first().pk
    #
    #     res = self.client.delete(
    #         get_delete_view_url(institute.institute_slug, subject.subject_slug, 'M1')
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_edit_view_name_success(self):
    #     """Test that editing view name is success by permitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     create_institute_subject_permission(self.user, self.user, subject)
    #
    #     res = self.client.patch(
    #         get_edit_subject_module_url(subject.subject_slug, 'MI'),
    #         {'name': 'newname'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data['name'], 'newname')
    #
    # def test_edit_view_name_fails_by_unpermitted_user(self):
    #     """Test that editing view name fails by unpermitted user"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #
    #     res = self.client.patch(
    #         get_edit_subject_module_url(subject.subject_slug, 'MI'),
    #         {'name': 'newname'}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_get_course_min_preview_details_by_admin_success(self):
    #     """Test that admin can get min preview details of course structure"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     ext_link = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     link = models.SubjectExternalLinkStudyMaterial.objects.create(
    #         external_link_study_material=ext_link,
    #         url='abc'
    #     )
    #
    #     res = self.client.get(
    #         get_course_preview_min_details(institute.institute_slug, subject.subject_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertIn('instructors', res.data)
    #     self.assertEqual(len(res.data['instructors']), 0)
    #     self.assertIn('view_order', res.data)
    #     self.assertEqual(len(res.data['view_order']), 3)
    #
    # def test_adding_of_course_content_question_success_by_permitted_user(self):
    #     """Test that adding course content question is successful by permitted user with active license"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     payload = {
    #         'question': 'What',
    #         'rgb_color': '(255, 255, 255, 0.5)',
    #         'anonymous': True,
    #         'description': 'a'
    #     }
    #     res = self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ), payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['question'], payload['question'])
    #     self.assertEqual(res.data['rgb_color'], payload['rgb_color'])
    #     self.assertEqual(res.data['description'], payload['description'])
    #     self.assertTrue(res.data['anonymous'])
    #     self.assertEqual(res.data['user'], 'Anonymous User')
    #     self.assertNotIn('user_id', res.data)
    #     self.assertIn('created_on', res.data)
    #
    # def test_adding_of_course_content_question_fails_by_permitted_user_no_active_license(self):
    #     """Test that adding course content question fails by permitted user with no active license"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     payload = {
    #         'question': 'What',
    #         'rgb_color': '(255, 255, 255, 0.5)',
    #         'anonymous': False,
    #         'description': 'a'
    #     }
    #     res = self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ),
    #         payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Active license not found or expired.')
    #
    # def test_adding_of_course_content_question_fails_by_permitted_user_no_expired_license(self):
    #     """Test that adding course content question fails by permitted user with expired license"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() - datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     payload = {
    #         'question': 'What',
    #         'rgb_color': '(255, 255, 255, 0.5)',
    #         'anonymous': False,
    #         'description': 'a'
    #     }
    #     res = self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ),
    #         payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Active license not found or expired.')
    #
    # def test_adding_of_course_content_question_fails_by_unpermitted_user(self):
    #     """Test that adding course content question fails by unpermitted user with active license"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     payload = {
    #         'question': 'What',
    #         'rgb_color': '(255, 255, 255, 0.5)',
    #         'anonymous': False,
    #         'description': 'a'
    #     }
    #     res = self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ),
    #         payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_duplicate_question_asking_fails(self):
    #     """Test that user can not ask duplicate question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     payload = {
    #         'question': 'What',
    #         'rgb_color': '(255, 255, 255, 0.5)',
    #         'anonymous': True,
    #         'description': 'a'
    #     }
    #     self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ), payload)
    #     res = self.client.post(
    #         get_institute_subject_content_ask_question_url(
    #             institute.institute_slug,
    #             subject.subject_slug,
    #             course_content.pk
    #         ), payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This question already exists.')
    #
    # def test_answering_question_by_permitted_user_success(self):
    #     """Test that answering questions by permitted user is successful"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     payload = {
    #         'answer': 'ans',
    #         'anonymous': True,
    #         'rgb_color': '(255, 255, 255, 0.5)'
    #     }
    #
    #     res = self.client.post(
    #         get_answer_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         payload
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['answer'], payload['answer'])
    #     self.assertEqual(res.data['rgb_color'], payload['rgb_color'])
    #     self.assertEqual(res.data['anonymous'], str(payload['anonymous']))
    #     self.assertEqual(res.data['user'], 'Anonymous User')
    #     self.assertEqual(res.data['content_question_id'], question.pk)
    #     self.assertEqual(res.data['role'], 'Instructor')
    #     self.assertFalse(res.data['pin'])
    #     self.assertNotIn('user_id', res.data)
    #     self.assertIn('id', res.data)
    #     self.assertIn('created_on', res.data)
    #
    # def test_answering_question_by_unpermitted_user_fails(self):
    #     """Test that answering questions by unpermitted user fails"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, self.user)
    #
    #     payload = {
    #         'answer': 'ans',
    #         'anonymous': True,
    #         'rgb_color': '(255, 255, 255, 0.5)'
    #     }
    #
    #     res = self.client.post(
    #         get_answer_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         payload
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_answering_question_by_permitted_user_twice_same_ans_fails(self):
    #     """Test that answering same ans to question by permitted user fails"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     payload = {
    #         'answer': 'ans',
    #         'anonymous': True,
    #         'rgb_color': '(255, 255, 255, 0.5)'
    #     }
    #
    #     self.client.post(
    #         get_answer_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         payload
    #     )
    #     res = self.client.post(
    #         get_answer_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         payload
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'This answer has already been posted.')
    #
    # def def_answering_question_with_no_active_license_fails(self):
    #     """Test that answering question with no active license fails."""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() - datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     payload = {
    #         'answer': 'ans',
    #         'anonymous': True,
    #         'rgb_color': '(255, 255, 255, 0.5)'
    #     }
    #
    #     res = self.client.post(
    #         get_answer_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         payload
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Active license not found or expired.')
    #
    # def test_upvote_question_success_by_permitted_user(self):
    #     """Test that permitted user can upvote question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['question_id'], question.pk)
    #     self.assertEqual(res.data['upvoted'], True)
    #
    # def test_upvote_self_question_fails_by_permitted_user(self):
    #     """Test that permitted user can not upvote self question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Bad Request.')
    #
    # def test_upvote_question_fails_by_unpermitted_user(self):
    #     """Test that un-permitted user can not upvote question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, admin)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_twice_upvote_question_fails_by_permitted_user(self):
    #     """Test that permitted user can not upvote question twice"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #
    #     self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Question already upvoted.')
    #
    # def test_remove_upvote_question_success_by_self(self):
    #     """Test that permitted user can remove upvote to question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #
    #     self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_remove_upvote_question_fails_by_non_self(self):
    #     """Test that permitted user can not remove upvote to question if upvote not self"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #
    #     self.client.force_authenticate(admin)
    #     self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.client.force_authenticate(self.user)
    #     res = self.client.post(
    #         get_upvote_downvote_question_url(institute.institute_slug, subject.subject_slug, question.pk),
    #         {}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_upvote_answer_success_by_permitted_user(self):
    #     """Test that permitted user can upvote answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data['answer_id'], answer.pk)
    #     self.assertEqual(res.data['upvoted'], True)
    #
    # def test_upvote_self_answer_fails_by_permitted_user(self):
    #     """Test that permitted user can not upvote self answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Bad Request.')
    #
    # def test_upvote_answer_fails_by_unpermitted_user(self):
    #     """Test that un-permitted user can not upvote answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_twice_upvote_answer_fails_by_permitted_user(self):
    #     """Test that permitted user can not upvote answer twice"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Answer already upvoted.')
    #
    # def test_remove_upvote_answer_success_by_self(self):
    #     """Test that permitted user can remove upvote to answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {}
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_remove_upvote_answer_fails_by_non_self(self):
    #     """Test that permitted user can not remove upvote to answer if upvote not self"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     self.client.force_authenticate(admin)
    #     self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {'upvote': True}
    #     )
    #
    #     self.client.force_authenticate(self.user)
    #     res = self.client.post(
    #         get_upvote_downvote_answer_url(institute.institute_slug, subject.subject_slug, answer.pk),
    #         {}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_question_success_by_self(self):
    #     """Test that asker of question can delete question"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     res = self.client.delete(
    #         get_delete_question_url(question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_delete_question_fails_by_non_self(self):
    #     """Test that asker of question can delete question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #
    #     res = self.client.delete(
    #         get_delete_question_url(question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_twice_question_success_by_self(self):
    #     """Test that asker of question can delete question twice"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #
    #     self.client.delete(
    #         get_delete_question_url(question.pk)
    #     )
    #     res = self.client.delete(
    #         get_delete_question_url(question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_delete_answer_success_by_self(self):
    #     """Test that answer provider or institute permitted user can delete answer"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     res = self.client.delete(
    #         get_delete_answer_url(subject.subject_slug, answer.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_delete_answer_success_by_instructor(self):
    #     """Test that answer provider or institute permitted user can delete answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.delete(
    #         get_delete_answer_url(subject.subject_slug, answer.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_delete_answer_fails_by_non_permitted_user(self):
    #     """Test that non answer provider can not delete question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.delete(
    #         get_delete_answer_url(subject.subject_slug, answer.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_delete_twice_question_success_by_self(self):
    #     """Test that can delete question twice"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     self.client.delete(
    #         get_delete_answer_url(subject.subject_slug, answer.pk)
    #     )
    #     res = self.client.delete(
    #         get_delete_answer_url(subject.subject_slug, answer.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    #
    # def test_asker_of_question_can_pin_answer(self):
    #     """Test that asker of question can pin answer"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(self.user, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #     other_user = create_teacher()
    #     answer = answer_question(question, other_user)
    #
    #     res = self.client.post(
    #         get_pin_answer_url(answer.pk),
    #         {}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #
    # def test_non_asker_of_question_can_not_pin_answer(self):
    #     """Test that asker of question can pin answer"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.post(
    #         get_pin_answer_url(answer.pk),
    #         {}
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_create_endpoint_for_listing_answers_to_question_success_by_admin(self):
    #     """Test that admin can list answers to question"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     res = self.client.get(
    #         get_answer_list_url(institute.institute_slug, subject.subject_slug, question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertTrue(res.data[0]['anonymous'])
    #     self.assertEqual(res.data[0]['answer'], answer.answer)
    #     self.assertEqual(res.data[0]['pin'], answer.pin)
    #
    # def test_create_endpoint_for_listing_answers_to_question_success_by_subject_incharge(self):
    #     """Test that subject incharge can list answers to question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.get(
    #         get_answer_list_url(institute.institute_slug, subject.subject_slug, question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertTrue(res.data[0]['anonymous'])
    #     self.assertEqual(res.data[0]['answer'], answer.answer)
    #     self.assertEqual(res.data[0]['pin'], answer.pin)
    #
    # def test_create_endpoint_for_listing_answers_to_question_fails_by_non_permitted_user(self):
    #     """Test that non user can not list answer to question"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.get(
    #         get_answer_list_url(institute.institute_slug, subject.subject_slug, question.pk)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_list_question_success_by_admin(self):
    #     """Test that admin can list all questions"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     res = self.client.get(
    #         get_question_list_url(institute.institute_slug, subject.subject_slug, course_content.pk)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['question'], question.question)
    #     self.assertEqual(res.data[0]['answer_count'], 1)
    #     self.assertEqual(res.data[0]['upvotes'], 0)
    #
    # def test_list_question_success_by_subject_incharge(self):
    #     """Test that subject incharge can list all questions"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     create_institute_subject_permission(admin, self.user, subject)
    #     question = ask_question(course_content, self.user)
    #     answer = answer_question(question, self.user)
    #
    #     res = self.client.get(
    #         get_question_list_url(institute.institute_slug, subject.subject_slug, course_content.pk)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['question'], question.question)
    #     self.assertEqual(res.data[0]['answer_count'], 1)
    #     self.assertEqual(res.data[0]['upvotes'], 0)
    #
    # def test_list_question_fails_by_non_permitted_user(self):
    #     """Test that non permitted user can not list all questions"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     order = create_order(lic, institute)
    #     order.paid = True
    #     order.payment_date = timezone.now()
    #     order.active = True
    #     order.end_date = timezone.now() + datetime.timedelta(days=10)
    #     order.save()
    #     class_ = create_class(institute)
    #     subject = create_subject(class_)
    #     view = models.SubjectViewNames.objects.filter(
    #         key='MI'
    #     ).first()
    #     course_content = models.InstituteSubjectCourseContent.objects.create(
    #         view=view,
    #         course_content_subject=subject,
    #         title='a',
    #         content_type='L'
    #     )
    #     question = ask_question(course_content, admin)
    #     answer = answer_question(question, admin)
    #
    #     res = self.client.get(
    #         get_question_list_url(institute.institute_slug, subject.subject_slug, course_content.pk)
    #     )
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')
    #
    # def test_get_class_key_value_pair_success_admin(self):
    #     """Test get class key value pair success by admin"""
    #     institute = create_institute(self.user)
    #     lic = create_institute_license(institute, self.payload)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_classes_key_value_url(institute.institute_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['class_slug'], class_.class_slug)
    #     self.assertEqual(res.data[0]['name'], class_.name)
    #
    # def test_get_class_key_value_pair_success_other_admin(self):
    #     """Test get class key value pair success by admin"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     class_ = create_class(institute)
    #     create_invite(institute, admin, self.user, models.InstituteRole.ADMIN)
    #     accept_invite(institute, self.user, models.InstituteRole.ADMIN)
    #
    #     res = self.client.get(
    #         get_classes_key_value_url(institute.institute_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['class_slug'], class_.class_slug)
    #     self.assertEqual(res.data[0]['name'], class_.name)
    #
    # def test_get_class_key_value_pair_fails_by_non_user(self):
    #     """Test get class key value pair fails by non user"""
    #     admin = create_teacher()
    #     institute = create_institute(admin)
    #     lic = create_institute_license(institute, self.payload)
    #     class_ = create_class(institute)
    #
    #     res = self.client.get(
    #         get_classes_key_value_url(institute.institute_slug)
    #     )
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(res.data['error'], 'Permission denied.')

    def test_add_student_to_institute_successful_by_admin(self):
        """Test that admin can add student in institute"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)
        student = create_student()

        payload = {
            'user': str(student),
            'class': class_.class_slug,
            'enrollment_no': '123e',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['user'], str(student))
        self.assertEqual(res.data['institute'], institute.institute_slug)
        self.assertEqual(res.data['first_name'], '')
        self.assertEqual(res.data['last_name'], '')
        self.assertEqual(res.data['enrollment_no'], payload['enrollment_no'])
        self.assertEqual(res.data['registration_no'], '')
        self.assertEqual(res.data['class'], class_.name)
        self.assertIn('created_on', res.data)

    def test_add_student_to_institute_twice_by_admin_fails(self):
        """Test that admin can add student in institute twice fails"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)
        student = create_student()

        payload = {
            'user': str(student),
            'class': class_.class_slug,
            'enrollment_no': '',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )
        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Student was already invited.')

    def test_add_already_added_student_to_institute_by_admin_fails(self):
        """Test that existing student can not be added again"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)
        student = create_student()

        payload = {
            'user': str(student),
            'class': class_.class_slug,
            'enrollment_no': '123e',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        models.InstituteStudents.objects.create(
            invitee=student,
            institute=institute,
            active=True
        )
        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Student was already invited.')

    def test_add_student_to_institute_by_non_permitted_user_fails(self):
        """Test that non permitted can add student in institute fails"""
        admin = create_teacher()
        institute = create_institute(admin)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)
        student = create_student()

        payload = {
            'user': str(student),
            'class': class_.class_slug,
            'enrollment_no': '123e',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Permission denied.')

    def test_add_teacher_to_institute_student_fails_by_admin(self):
        """Test that add teacher as student in institute fails"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)
        teacher = create_teacher()

        payload = {
            'user': str(teacher),
            'class': class_.class_slug,
            'enrollment_no': '123e',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'User is not a student.')

    def test_add_invalid_user_to_institute_student_fails_by_admin(self):
        """Test that add invalid user as student in institute fails"""
        institute = create_institute(self.user)
        lic = create_institute_license(institute, self.payload)
        order = create_order(lic, institute)
        order.paid = True
        order.payment_date = timezone.now()
        order.save()
        class_ = create_class(institute)

        payload = {
            'user': 'absdffd@sfsdf.com',
            'class': class_.class_slug,
            'enrollment_no': '123e',
            'registration_no': '',
            'first_name': '',
            'last_name': ''
        }

        res = self.client.post(
            get_add_student_to_institute_url(institute.institute_slug),
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'No student with this email was found.')
