import os
import random
import string
import time
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import EmailValidator, MinLengthValidator, \
    ProhibitNullCharactersValidator, validate_image_file_extension
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.contrib.auth.hashers import make_password, check_password
from unixtimestampfield.fields import UnixTimeStampField

from app import settings

from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from .tasks import create_welcome_message_after_user_creation

# Constant to define unlimited limit
UNLIMITED = 99999

class Temp(viewsets.ModelViewSet):
    pass


class OperationalCountries(Countries):
    """Overriding countries to include only operational countries."""
    only = ['IN', ]


# Languages available as options in language field
class Languages:
    ENGLISH = 'EN'
    BENGALI = 'BN'
    HINDI = 'HI'
    LANGUAGE_IN_LANGUAGE_CHOICES = [
        (ENGLISH, _(u'English')),
        (BENGALI, _(u'Bengali')),
        (HINDI, _(u'Hindi'))
    ]


# Gender available as options in Gender Field
class Gender:
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    NOT_MENTIONED = ''

    GENDER_IN_GENDER_CHOICES = [
        (MALE, _(u'Male')),
        (FEMALE, _(u'Female')),
        (OTHER, _(u'Other')),
        (NOT_MENTIONED, _(u'Not Mentioned'))
    ]


# States available as options in state field
class StatesAndUnionTerritories:
    ANDAMAN_AND_NICOBAR_ISLANDS = 'AN'
    ANDHRA_PRADESH = 'AP'
    ARUNACHAL_PRADESH = 'AR'
    ASSAM = 'AS'
    BIHAR = 'BR'
    CHANDIGARH = 'CH'
    CHHATTISGARH = 'CT'
    DADRA_AND_NAGAR_HAVELI = 'DN'
    DAMAN_AND_DIU = 'DD'
    DELHI = 'DL'
    GOA = 'GA'
    GUJARAT = 'GJ'
    HARYANA = 'HR'
    HIMACHAL_PRADESH = 'HP'
    JAMMU_AND_KASHMIR = 'JK'
    JHARKHAND = 'JH'
    KARNATAKA = 'KA'
    KERALA = 'KL'
    LAKSHADWEEP = 'LD'
    MADHYA_PRADESH = 'MP'
    MAHARASHTRA = 'MH'
    MANIPUR = 'MR'
    MEGHALAYA = 'ML'
    MIZORAM = 'MZ'
    NAGALAND = 'NL'
    ODISHA = 'OR'
    PONDICHERRY = 'PD'
    PUNJAB = 'PB'
    RAJASHTAN = 'RJ'
    SIKKIM = 'SK'
    TAMIL_NADU = 'TN'
    TELANGANA = 'TG'
    TRIPURA = 'TR'
    UTTAR_PRADESH = 'UP'
    UTTARAKHAND = 'UK'
    WEST_BENGAL = 'WB'

    STATE_IN_STATE_CHOICES = [
        (ANDAMAN_AND_NICOBAR_ISLANDS,
         _(u'Andaman and Nicobar Islands')),
        (ANDHRA_PRADESH, _(u'Andhra Pradesh')),
        (ARUNACHAL_PRADESH, _(u'Arunachal Pradesh')),
        (ASSAM, _(u'Assam')),
        (BIHAR, _(u'Bihar')),
        (CHANDIGARH, _(u'Chandigarh')),
        (CHHATTISGARH, _(u'Chhattishgarh')),
        (DADRA_AND_NAGAR_HAVELI, _(u'Dadra and Nagar Haveli')),
        (DAMAN_AND_DIU, _(u'Daman and Diu')),
        (GOA, _(u'Goa')),
        (GUJARAT, _(u'Gujarat')),
        (HARYANA, _(u'Haryana')),
        (HIMACHAL_PRADESH, _(u'Himachal Pradesh')),
        (JAMMU_AND_KASHMIR, _(u'Jammu and Kashmir')),
        (JHARKHAND, _(u'Jharkhand')),
        (KARNATAKA, _(u'Karnataka')),
        (KERALA, _(u'Kerala')),
        (LAKSHADWEEP, _(u'Lakshadweep')),
        (MADHYA_PRADESH, _(u'Madhya Pradesh')),
        (MAHARASHTRA, _(u'Maharashtra')),
        (MANIPUR, _(u'Manipur')),
        (MEGHALAYA, _(u'Meghalaya')),
        (MIZORAM, _(u'Mizoram')),
        (NAGALAND, _(u'Nagaland')),
        (ODISHA, _(u'Odisha')),
        (PONDICHERRY, _(u'Pondicherry')),
        (PUNJAB, _(u'Punjab')),
        (RAJASHTAN, _(u'Rajasthan')),
        (SIKKIM, _(u'Sikkim')),
        (TAMIL_NADU, _(u'Tamil Nadu')),
        (TELANGANA, _(u'Telangana')),
        (TRIPURA, _(u'Tripura')),
        (UTTAR_PRADESH, _(u'Uttar Pradesh')),
        (UTTARAKHAND, _(u'Uttarakhand')),
        (WEST_BENGAL, _(u'West Bengal')),
    ]


class InstituteCategory:
    EDUCATION = 'E'
    ART = 'A'
    MUSIC = 'M'
    DANCE = 'D'
    CATEGORY_IN_INSTITUTE_CATEGORIES = [
        (EDUCATION, _(u'EDUCATION')),
        (ART, _(u'ART')),
        (MUSIC, _(u'MUSIC')),
        (DANCE, _(u'DANCE'))
    ]


class InstituteType:
    SCHOOL = 'SC'
    COLLEGE = 'CO'
    COACHING = 'CC'

    TYPE_IN_INSTITUTE_TYPE = [
        (SCHOOL, _(u'SCHOOL')),
        (COLLEGE, _(u'COLLEGE')),
        (COACHING, _(u'COACHING')),
    ]


class InstituteRole:
    ADMIN = 'A'
    STAFF = 'S'
    FACULTY = 'F'

    ROLE_IN_INSTITUTE_ROLES = [
        (ADMIN, _(u'ADMIN')),
        (STAFF, _(u'STAFF')),
        (FACULTY, _(u'FACULTY')),
    ]


class InstituteSubjectType:
    OPTIONAL = 'O'
    MANDATORY = 'M'

    SUBJECT_TYPE_IN_INSTITUTE_SUBJECTS = [
        (OPTIONAL, _(u'OPTIONAL')),
        (MANDATORY, _(u'MANDATORY'))
    ]


class Billing:
    MONTHLY = 'M'
    ANNUALLY = 'A'

    BILLING_MODES_IN_INSTITUTE_BILLING = [
        (MONTHLY, _(u'MONTHLY')),
        (ANNUALLY, _(u'ANNUALLY'))
    ]


class InstituteLicenseTypes:
    NOT_PURCHASED = 'N'
    SELECTED = 'S'
    ACTIVE = 'A'
    EXPIRED = 'E'

    LICENSE_TYPE_IN_LICENSE_TYPES = [
        (NOT_PURCHASED, _(u'NOT_PURCHASED')),
        (SELECTED, _(u'SELECTED')),
        (ACTIVE, _(u'ACTIVE')),
        (EXPIRED, _(u'EXPIRED')),
    ]


class InstituteLicensePlans:
    BASIC = 'BAS'
    BUSINESS = 'BUS'
    ENTERPRISE = 'ENT'

    LICENSE_PLANS_IN_INSTITUTE_LICENSE = [
        (BASIC, _(u'BASIC')),
        (BUSINESS, _(u'BUSINESS')),
        (ENTERPRISE, _(u'ENTERPRISE'))
    ]


class PaymentGateway:
    RAZORPAY = 'R'

    PAYMENT_GATEWAY_IN_PAYMENT_GATEWAYS = [
        (RAZORPAY, _(u'RAZORPAY')),
    ]


class ProductTypes:
    LMS_CMS_EXAM_LIVE_STREAM = 'A'
    DIGITAL_EXAM = 'E'
    LIVE_STREAM = 'L'
    STORAGE = 'S'
    NOT_SELECTED = 'N'

    PRODUCT_TYPE_IN_PRODUCT_TYPES = [
        (LMS_CMS_EXAM_LIVE_STREAM, _(u'LMS_CMS_EXAM_LIVE_STREAM')),
        (DIGITAL_EXAM, _(u'DIGITAL_EXAM')),
        (LIVE_STREAM, _(u'LIVE_STREAM')),
        (STORAGE, _(u'STORAGE')),
        (NOT_SELECTED, _(u'NOT_SELECTED')),
    ]


class SubjectViewType:
    MODULE_VIEW = 'M'
    TEST_VIEW = 'T'

    VIEW_TYPE_IN_VIEW_TYPES = [
        (MODULE_VIEW, _(u'MODULE_VIEW')),
        (TEST_VIEW, _(u'TEST_VIEW'))
    ]


class SubjectModuleViewType:
    LECTURE_VIEW = 'L'
    TEST_VIEW = 'T'

    VIEW_TYPE_IN_VIEW_TYPES = [
        (LECTURE_VIEW, _(u'LECTURE_VIEW')),
        (TEST_VIEW, _(u'TEST_VIEW'))
    ]


class SubjectLectureMaterialsContentType:
    IMAGE = 'I'
    PDF = 'P'
    EXTERNAL_LINK = 'E'
    YOUTUBE_LINK = 'Y'
    LIVE_CLASS = 'L'

    CONTENT_TYPE_IN_CONTENT_TYPES = [
        (IMAGE, _(u'IMAGE')),
        (PDF, _(u'PDF')),
        (EXTERNAL_LINK, _(u'EXTERNAL_LINK')),
        (YOUTUBE_LINK, _(u'YOUTUBE_LINK')),
        (LIVE_CLASS, _(u'LIVE_CLASS')),
    ]


class SubjectIntroductionContentType:
    IMAGE = 'I'
    PDF = 'P'
    LINK = 'L'

    CONTENT_TYPE_IN_CONTENT_TYPES = [
        (IMAGE, _(u'IMAGE')),
        (PDF, _(u'PDF')),
        (LINK, _(u'LINK'))
    ]


class SubjectLectureUseCaseOrObjectives:
    USE_CASE = 'U'
    OBJECTIVES = 'O'

    VIEW_TYPE_IN_VIEW_TYPES = [
        (USE_CASE, _(u'USE_CASE')),
        (OBJECTIVES, _(u'OBJECTIVES'))
    ]


class SubjectAdditionalReadingOrUseCaseLinkType:
    ADDITIONAL_READING_LINK = 'A'
    USE_CASES_LINK = 'U'

    LINK_VIEW_TYPE_IN_LINK_VIEW_TYPES = [
        (ADDITIONAL_READING_LINK, _(u'ADDITIONAL_READING_LINK')),
        (USE_CASES_LINK, _(u'USE_CASES_LINK'))
    ]


class SubjectAssignmentType:
    MANDATORY = 'A'
    OPTIONAL = 'U'

    ASSIGNMENT_TYPE_IN_SUBJECT_ASSIGNMENT_TYPES = [
        (MANDATORY, _(u'MANDATORY')),
        (OPTIONAL, _(u'OPTIONAL'))
    ]


class GradedType:
    GRADED = 'G'
    UNGRADED = 'U'

    GRADED_TYPE_IN_GRADED_TYPES = [
        (GRADED, _(u'GRADED')),
        (UNGRADED, _(u'UNGRADED'))
    ]


class TestScheduleType:
    SPECIFIC_DATE_AND_TIME = 'DT'
    SPECIFIC_DATE = 'D'
    UNSCHEDULED = 'UN'

    TYPE_IN_TEST_SCHEDULE_TYPES = [
        (SPECIFIC_DATE_AND_TIME, _(u'SPECIFIC_DATE_AND_TIME')),
        (SPECIFIC_DATE, _(u'SPECIFIC_DATE')),
        (UNSCHEDULED, _(u'UNSCHEDULED')),
    ]


class StudyMaterialView:
    MEET_YOUR_INSTRUCTOR = 'MI'
    COURSE_OVERVIEW = 'CO'

    STUDY_MATERIAL_VIEW_TYPES = [
        (MEET_YOUR_INSTRUCTOR, _(u'MEET_YOUR_INSTRUCTOR')),
        (COURSE_OVERVIEW, _(u'COURSE_OVERVIEW'))
    ]


class QuestionMode:
    TYPED = 'T'
    IMAGE = 'I'
    FILE = 'F'

    QUESTION_MODE_IN_QUESTION_MODES = [
        (TYPED, _(u'TYPED')),
        (IMAGE, _(u'IMAGE')),
        (FILE, _(u'FILE'))
    ]


class AnswerMode:
    TYPED = 'T'
    FILE = 'F'

    ANSWER_MODE_IN_ANSWER_MODES = [
        (TYPED, _(u'TYPED')),
        (FILE, _(u'FILE'))
    ]


class QuestionCategory:
    AUTOCHECK_TYPE = 'A'
    ALL_TYPES = 'Z'
    FILE_UPLOAD_TYPE = 'F'

    QUESTION_CATEGORY_IN_QUESTION_CATEGORIES = [
        (AUTOCHECK_TYPE, _(u'AUTOCHECK_TYPE')),
        (ALL_TYPES, _(u'ALL_TYPES')),
        (FILE_UPLOAD_TYPE, _(u'FILE_UPLOAD_TYPE'))
    ]


class TestQuestionSectionType:
    OPTIONAL = 'O'
    MANDATORY = 'M'

    TYPE_IN_SECTION_TYPES = [
        (OPTIONAL, _(u'OPTIONAL')),
        (MANDATORY, _(u'MANDATORY'))
    ]


class QuestionType:
    MCQ = 'M'
    TRUE_FALSE = 'T'
    SELECT_MULTIPLE_CHOICE = 'M'
    FILL_IN_THE_BLANK = 'F'
    ASSERTION = 'A'
    SHORT_ANSWER = 'S'
    DESCRIPTIVE_ANSWER = 'D'
    NUMERIC_ANSWER = 'N'
    PICTURE_TYPE_QUESTION = 'P'

    TYPE_IN_QUESTION_TYPES = [
        (MCQ, _(u'MCQ')),
        (TRUE_FALSE, _(u'TRUE_FALSE')),
        (SELECT_MULTIPLE_CHOICE, _(u'SELECT_MULTIPLE_CHOICE')),
        (FILL_IN_THE_BLANK, _(u'FILL_IN_THE_BLANK')),
        (ASSERTION, _(u'ASSERTION')),
        (SHORT_ANSWER, _(u'SHORT_ANSWER')),
        (DESCRIPTIVE_ANSWER, _(u'DESCRIPTIVE_ANSWER')),
        (NUMERIC_ANSWER, _(u'NUMERIC_ANSWER')),
        (PICTURE_TYPE_QUESTION, _(u'PICTURE_TYPE_QUESTION'))
    ]


class TestPlace:
    GLOBAL = 'G'
    LECTURE = 'L'
    MODULE = 'M'

    PLACES_IN_PLACE_TYPES = [
        (GLOBAL, _(u'GLOBAL')),
        (LECTURE, _(u'LECTURE')),
        (MODULE, _(u'MODULE'))
    ]


def user_profile_picture_upload_file_path(instance, filename):
    """Generates file path for uploading images in user profile"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'pictures/uploads/user/profile'
    full_path = os.path.join(path, file_name)

    return full_path


def institute_logo_upload_file_path(instance, filename):
    """Generates file path for uploading institute logo"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'pictures/uploads/institute/logo'
    full_path = os.path.join(path, file_name)

    return full_path


def institute_banner_upload_file_path(instance, filename):
    """Generates file path for uploading institute banner"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'pictures/uploads/institute/banner'
    full_path = os.path.join(path, file_name)

    return full_path


def subject_img_study_material_upload_file_path(instance, filename):
    """Generates file path for uploading institute image study material"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'institute/uploads/content/image'
    full_path = os.path.join(path, file_name)
    return full_path


def subject_introductory_content_upload_file_path(instance, filename):
    """Generates file path for uploading institute introductory content"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'institute/uploads/content/introduction'
    full_path = os.path.join(path, file_name)
    return full_path


def subject_pdf_study_material_upload_file_path(instance, filename):
    """Generates file path for uploading institute pdf study material"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'institute/uploads/content/pdf'
    full_path = os.path.join(path, file_name)
    return full_path


def hls_encoded_video_saving_file_name_path(filename):
    """Generates file name and path for uploading hls encoded media"""
    extension = filename.split('.')[-1]
    name = filename.split('/')[-1].strip('.' + extension)
    path = settings.MEDIA_ROOT + '/' + 'institute/uploads/content/video/hls/' + name + '/'
    full_path = os.path.join(path, name + '.m3u8')
    return full_path


def hls_key_saving_path(filename):
    """Generates path to save keys"""
    extension = filename.split('.')[-1]
    name = filename.split('/')[-1].strip('.' + extension)
    full_path = settings.MEDIA_ROOT + '/' + 'institute/uploads/content/video/hls-encryption-keys/' + name + '/key'
    return full_path


def subject_file_test_question_file_path(instance, filename):
    """Generates file path for uploading subject test file question paper"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'institute/uploads/test/question_paper/file'
    full_path = os.path.join(path, file_name)
    return full_path


def subject_image_test_question_file_path(instance, filename):
    """Generates file path for uploading subject test image question"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    path = 'institute/uploads/test/question_paper/image'
    full_path = os.path.join(path, file_name)
    return full_path


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_for_institute(instance, new_slug=None):
    """Generates unique slug field for institute"""
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    k_class = instance.__class__
    qs_exists = k_class.objects.filter(institute_slug=slug).exists()

    if qs_exists:
        new_slug = f'{slug}-{random_string_generator(size=6)}'
        return unique_slug_generator_for_institute(
            instance, new_slug=new_slug
        )
    return slug


def unique_coupon_code_generator(instance):
    """Generates and returns a new coupon code"""
    while True:
        slug = 'I' + random_string_generator(size=5).upper()

        k_class = instance.__class__
        qs_exists = k_class.objects.filter(coupon_code=slug).exists()

        if not qs_exists:
            break
    return slug


def unique_slug_generator_for_test_set(instance):
    """Generates and returns a new test set slug"""
    while True:
        slug = random_string_generator(size=8).upper()

        k_class = instance.__class__
        qs_exists = k_class.objects.filter(set_slug=slug).exists()

        if not qs_exists:
            break
    return slug


def generate_student_test_password(instance):
    """Generates and returns a new test set slug"""
    while True:
        hashed_password = make_password(random_string_generator(size=6).upper())

        k_class = instance.__class__
        qs_exists = k_class.objects.filter(test=instance.test, password=hashed_password).exists()

        if not qs_exists:
            break
    return hashed_password


def create_order_receipt(instance):
    """Generates unique receipt id for institute"""
    while True:
        order_receipt = 'order_rcptidins' + random_string_generator(size=10)
        k_class = instance.__class__
        qs_exists = k_class.objects.filter(order_receipt=order_receipt).exists()

        if not qs_exists:
            break
    return order_receipt


def unique_key_generator_for_subject_view_name(subject):
    """Generates unique key for subject view"""
    while True:
        key = random_string_generator(size=6)
        qs_exists = SubjectViewNames.objects.filter(
            view_subject=subject,
            key=key
        ).exists()
        if not qs_exists:
            break
    return key


def unique_slug_generator_for_class(instance):
    """Generates a unique slug for class"""
    while True:
        slug = f'{slugify(instance.name)}-{random_string_generator(size=4)}-{random_string_generator(size=4)}'
        k_class = instance.__class__
        qs_exists = k_class.objects.filter(class_slug=slug).exists()

        if not qs_exists:
            break
    return slug


def unique_slug_generator_for_subject(instance):
    """Generates unique slug for subject"""
    while True:
        slug = f'{slugify(instance.name)}-{random_string_generator(size=8)}'
        k_class = instance.__class__
        qs_exists = k_class.objects.filter(subject_slug=slug).exists()

        if not qs_exists:
            break
    return slug


def unique_slug_generator_for_section(instance):
    """Generates unique slug for section"""
    while True:
        slug = f'{slugify(instance.name)}-{random_string_generator(size=4)}-{random_string_generator(size=4)}'
        k_class = instance.__class__
        qs_exists = k_class.objects.filter(section_slug=slug).exists()

        if not qs_exists:
            break
    return slug


def generate_test_slug(instance):
    """Generates unique test slug"""
    while True:
        slug = 'test-' + random_string_generator(5)
        k_class = instance.__class__
        qs_exists = k_class.objects.filter(test_slug=slug).exists()

        if not qs_exists:
            break
    return slug


class UserManager(BaseUserManager):

    def create_user(self, email, password, username, **extra_kwargs):
        """Creates and saves a new user"""

        if not email:
            raise ValueError(_('Email cannot be empty'))

        if not username:
            raise ValueError(_('Username cannot be empty'))

        user = self.model(email=self.normalize_email(email),
                          username=username, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)

        return user

    def create_superuser(self, email, password, username, **extra_kwargs):
        """Creates and saves a new user with superuser permission"""
        user = self.create_user(
            email, password, username, **extra_kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Creates user model that supports using email as username"""
    email = models.EmailField(_('Email'),
                              max_length=255, unique=True,
                              validators=(EmailValidator,))
    username = models.CharField(_('Username'), max_length=30, unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    is_student = models.BooleanField(_('Is Student'), default=False)
    is_teacher = models.BooleanField(_('Is Teacher'), default=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        """String representation of user model"""
        return self.email

    class Meta:
        permissions = (
            ('is_active', 'user_is_active'),
            ('is_staff', 'user_is_staff'),
            ('is_student', 'user_is_student'),
            ('is_teacher', 'user_is_teacher'),
        )


class UserProfile(models.Model, Languages):
    """Creates user profile model"""
    user = models.OneToOneField(
        'User',
        related_name='user_profile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        _('First Name'), max_length=70, blank=True, default='',
        validators=(ProhibitNullCharactersValidator,))
    last_name = models.CharField(
        _('Last Name'), max_length=70, blank=True, default='',
        validators=(ProhibitNullCharactersValidator,))
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        blank=True,
        default=Gender.NOT_MENTIONED,
        choices=Gender.GENDER_IN_GENDER_CHOICES, )
    phone = PhoneNumberField(_('Phone'), null=True, blank=True)
    date_of_birth = models.DateField(
        _('Date of Birth'), max_length=10, null=True, blank=True)
    country = CountryField(
        _('Country'), countries=OperationalCountries, default='IN')
    primary_language = models.CharField(
        _('Primary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        default=Languages.ENGLISH,
        blank=True
    )
    secondary_language = models.CharField(
        _('Secondary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        null=True, blank=True
    )
    tertiary_language = models.CharField(
        _('Tertiary language'),
        max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        """Overriding save method"""
        if self.first_name:
            self.first_name = self.first_name.upper().strip()

        if self.last_name:
            self.last_name = self.last_name.upper().strip()

        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        """String representation"""
        return str(self.user)


class SystemMessage(models.Model):
    """Model for storing system messages"""
    sender = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        'User',
        related_name='system_messages',
        on_delete=models.CASCADE
    )
    title = models.CharField(_('Title'), max_length=30)
    message = models.TextField(_('Message'), max_length=60)
    seen = models.BooleanField(_('Seen'), default=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)

    def __str__(self):
        return str(receiver)


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        # Creating user profile
        UserProfile.objects.create(user=instance)

        # Creates welcome message using task queue
        if instance.username != os.environ.get('SYSTEM_USER_USERNAME'):
            create_welcome_message_after_user_creation.delay(instance.pk)
    else:
        # Saving teacher profile and creating if not existing
        if instance.is_teacher:
            try:
                instance.user_profile.save()
            except ObjectDoesNotExist:
                UserProfile.objects.create(user=instance)


################################################################
#  Institute License
################################################################
class InstituteLicenseStat(models.Model):
    """For storing different kind of license statistics of institute"""
    institute = models.OneToOneField(
        'Institute', related_name='license_statistics_of_institute',
        on_delete=models.CASCADE)
    exam_license_stat = models.CharField(
        _('Exam license statistics'),
        max_length=1,
        choices=InstituteLicenseTypes.LICENSE_TYPE_IN_LICENSE_TYPES,
        default=InstituteLicenseTypes.NOT_PURCHASED,
        blank=True)
    live_stream_license_stat = models.CharField(
        _('Live stream license statistics'),
        max_length=1,
        choices=InstituteLicenseTypes.LICENSE_TYPE_IN_LICENSE_TYPES,
        default=InstituteLicenseTypes.NOT_PURCHASED,
        blank=True)
    all_product_license_stat = models.CharField(
        _('All products license statistics'),
        max_length=1,
        choices=InstituteLicenseTypes.LICENSE_TYPE_IN_LICENSE_TYPES,
        default=InstituteLicenseTypes.NOT_PURCHASED,
        blank=True)
    total_storage = models.DecimalField(
        _('Total storage in GB'), max_digits=13, decimal_places=9,
        default=0.0, blank=True)
    storage_license_end_date = UnixTimeStampField(
        _('Storage end date'), default=0, blank=True, use_numeric=True)

    def __str__(self):
        return str(self.institute)


class InstituteCommonLicense(models.Model):
    """Creates institute license model to store pricing structure"""
    user = models.ForeignKey(
        'User', related_name='institute_licenses', on_delete=models.CASCADE)
    type = models.CharField(
        _('Type'), max_length=3,
        choices=InstituteLicensePlans.LICENSE_PLANS_IN_INSTITUTE_LICENSE)
    billing = models.CharField(
        _('Billing'), max_length=1,
        choices=Billing.BILLING_MODES_IN_INSTITUTE_BILLING)
    price = models.BigIntegerField(_('Amount In Rs'))
    discount_percent = models.DecimalField(
        _('Discount In Percentage'), default=0.0,
        max_digits=5, decimal_places=2)
    gst_percent = models.DecimalField(
        _('GST in percentage'), default=0.0, max_digits=5, decimal_places=2)
    no_of_admin = models.PositiveIntegerField(
        _('No of admin'), default=1, blank=True)
    no_of_staff = models.PositiveIntegerField(
        _('No of staff'), default=0, blank=True)
    no_of_faculty = models.PositiveIntegerField(
        _('No of faculty'), default=0, blank=True)
    no_of_student = models.PositiveIntegerField(
        _('No of students'), default=UNLIMITED, blank=True)
    no_of_board_of_members = models.PositiveIntegerField(
        _('No of external board of members'), default=0, blank=True)
    video_call_max_attendees = models.PositiveIntegerField(
        _('Video call max attendees'), blank=False, null=False)
    classroom_limit = models.PositiveIntegerField(
        _('Classroom Limit'), default=UNLIMITED, blank=True)
    department_limit = models.PositiveIntegerField(
        _('Department Limit'), default=0, blank=True)
    subject_limit = models.PositiveIntegerField(
        _('Subject Limit'), default=UNLIMITED, blank=True)
    digital_test = models.BooleanField(
        _('Digital Test'), default=True, blank=True)
    LMS_exists = models.BooleanField(
        _('LMS exists'), default=True, blank=True)
    CMS_exists = models.BooleanField(
        _('CMS exists'), default=True, blank=True)
    discussion_forum = models.BooleanField(
        _('Discussion forum exists'), default=True, blank=True)

    def save(self, *args, **kwargs):
        """Overriding save method to allow only superuser
        to create license"""
        if not User.objects.get(email=self.user).is_superuser:
            raise PermissionDenied()

        return super(InstituteCommonLicense, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.type)

    class Meta:
        unique_together = ('type', 'billing')


class InstituteDiscountCoupon(models.Model):
    """
    Creates discount coupon model to store discount
    coupon in Rs for institute.
    """
    user = models.ForeignKey(
        'User', related_name='institute_discount_coupon',
        on_delete=models.SET_NULL, null=True)
    discount_rs = models.BigIntegerField(_('Discount in Rupees'), null=False)
    created_date = UnixTimeStampField(
        _('Created Date'), auto_now_add=True, use_numeric=True, editable=False)
    expiry_date = UnixTimeStampField(
        _('Expiry Date'), use_numeric=True, null=False)
    coupon_code = models.SlugField(
        _('Coupon Code'), blank=True, null=False, unique=True)
    active = models.BooleanField(_('Active'), default=True, blank=True)

    def save(self, *args, **kwargs):
        """Overrides save method"""
        if not self.discount_rs:
            raise ValueError({'discount_rs': _('This field is required.')})

        if not self.user:
            raise ValueError({'user': _('This field is required.')})

        if not self.expiry_date:
            raise ValueError({'expiry_date': _('This field is required.')})

        user = User.objects.get(email=self.user)
        if not (user.is_superuser or user.is_staff):
            raise PermissionDenied()

        super(InstituteDiscountCoupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.coupon_code


@receiver(pre_save, sender=InstituteDiscountCoupon)
def create_discount_coupon_code(sender, instance, *args, **kwargs):
    if not instance.coupon_code:
        coupon_code = unique_coupon_code_generator(instance)
        instance.coupon_code = coupon_code


class InstituteSelectedCommonLicense(models.Model):
    """
    Create institute selected license model to store
    selected license plans at that moment
    """
    institute = models.ForeignKey(
        'Institute', related_name='institute_selected_license',
        on_delete=models.CASCADE)
    type = models.CharField(
        _('Type'), max_length=3,
        choices=InstituteLicensePlans.LICENSE_PLANS_IN_INSTITUTE_LICENSE)
    billing = models.CharField(
        _('Billing'), max_length=1,
        choices=Billing.BILLING_MODES_IN_INSTITUTE_BILLING)
    price = models.DecimalField(  # In Rs
        _('Price In Rs'), max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(
        _('Discount In Percentage'), default=0.0,
        max_digits=5, decimal_places=2)
    discount_coupon = models.OneToOneField(
        to='InstituteDiscountCoupon', on_delete=models.SET_NULL,
        blank=True, null=True)
    gst_percent = models.DecimalField(
        _('GST in percentage'), default=0.0, max_digits=5, decimal_places=2)
    net_amount = models.DecimalField(
        _('Net Amount in Rs'), max_digits=10, decimal_places=2,
        blank=True, null=True)
    no_of_admin = models.PositiveIntegerField(_('No of admin'))
    no_of_staff = models.PositiveIntegerField(_('No of staff'))
    no_of_faculty = models.PositiveIntegerField(_('No of faculty'))
    no_of_student = models.PositiveIntegerField(_('No of students'))
    no_of_board_of_members = models.PositiveIntegerField(
        _('No of external board of members'), default=0, blank=True)
    video_call_max_attendees = models.PositiveIntegerField(_('Video call max attendees'))
    classroom_limit = models.PositiveIntegerField(_('Classroom Limit'))
    department_limit = models.PositiveIntegerField(_('Department Limit'))
    subject_limit = models.PositiveIntegerField(_('Subject Limit'), default=UNLIMITED, blank=True)
    digital_test = models.BooleanField(_('Digital Test'), default=True)
    LMS_exists = models.BooleanField(_('LMS exists'), default=True, blank=True)
    CMS_exists = models.BooleanField(_('CMS exists'), default=True, blank=True)
    discussion_forum = models.BooleanField(_('Discussion forum exists'), default=True, blank=True)
    payment_id_generated = models.BooleanField(_('Payment id generated'), default=False, blank=True)
    created_on = UnixTimeStampField(_('Created on'), use_numeric=True)

    def save(self, *args, **kwargs):
        if self.discount_coupon:
            if not self.discount_coupon.active:
                raise ValueError({'discount_coupon': _('Coupon already used.')})

            if timezone.now() > self.discount_coupon.expiry_date:
                raise ValueError({'discount_coupon': _('Coupon expired.')})

        super(InstituteSelectedCommonLicense, self).save(*args, **kwargs)

    def __str__(self):
        return 'License: ' + str(self.type) + ', billed: ' + str(self.billing)


@receiver(post_save, sender=InstituteSelectedCommonLicense)
def calculate_net_amount(sender, instance, created, *args, **kwargs):
    """Calculates net amount to be paid"""
    if created and not instance.net_amount:
        if instance.discount_coupon:
            instance.net_amount = max(0, instance.price * (
                    1 - (instance.discount_percent + instance.gst_percent) / 100) -
                                      instance.discount_coupon.discount_rs)
        else:
            instance.net_amount = max(0, instance.price * (
                    1 - (instance.discount_percent + instance.gst_percent) / 100))
        instance.save()

        if instance.discount_coupon:
            instance.discount_coupon.active = False
            instance.discount_coupon.save()


class InstituteCommonLicenseOrderDetails(models.Model):
    """Model to store institute common license order"""
    order_receipt = models.CharField(
        _('Order receipt'), max_length=30, blank=True, null=False)
    order_id = models.CharField(
        _('Order Id'), max_length=100, blank=True, null=False)
    amount = models.DecimalField(
        _('Amount in Rupees'), max_digits=10, decimal_places=2, blank=True, null=False)
    currency = models.CharField(_('Currency'), default='INR', blank=True, max_length=4)
    institute = models.ForeignKey(
        'Institute', on_delete=models.SET_NULL,
        related_name='institute_license_order', null=True)
    selected_license = models.OneToOneField(
        to='InstituteSelectedCommonLicense', on_delete=models.CASCADE, null=False)
    payment_gateway = models.CharField(
        _('Payment gateway'), max_length=1,
        choices=PaymentGateway.PAYMENT_GATEWAY_IN_PAYMENT_GATEWAYS)
    active = models.BooleanField(_('Active'), default=False, blank=True)
    paid = models.BooleanField(_('Paid'), default=False, blank=True)
    order_created_on = UnixTimeStampField(
        _('Order Created On'), auto_now_add=True, use_numeric=True, editable=False)
    payment_date = UnixTimeStampField(
        _('Payment Date'), use_numeric=True, null=True, blank=True)
    start_date = UnixTimeStampField(
        _('License Start Date'), use_numeric=True, blank=True, null=True)
    end_date = UnixTimeStampField(
        _('License Expiry Date'), use_numeric=True, blank=True, null=True)

    def __str__(self):
        return self.order_receipt

    class Meta:
        unique_together = ('institute', 'selected_license')


@receiver(pre_save, sender=InstituteCommonLicenseOrderDetails)
def create_unique_receipt_id(sender, instance, *args, **kwargs):
    """Creates unique order id for institute"""
    if not instance.amount:
        instance.amount = instance.selected_license.net_amount
    if not instance.order_receipt:
        instance.order_receipt = create_order_receipt(instance)
    if not instance.order_id:
        if instance.payment_gateway == PaymentGateway.RAZORPAY:
            order = settings.client.order.create(
                data={
                    'amount': float(instance.amount) * 100,
                    'currency': instance.currency,
                    'receipt': instance.order_receipt,
                    'notes': {'institute': instance.institute.institute_slug,
                              'selected_license': str(instance.selected_license)},
                    'payment_capture': '1'
                })
            instance.order_id = order['id']


class RazorpayCallback(models.Model):
    """Stores Razorpay callback credentials"""
    razorpay_order_id = models.CharField(
        _('Razorpay order id'), max_length=100,
        blank=False, null=False)
    razorpay_payment_id = models.CharField(
        _('Razorpay payment id'), max_length=100,
        blank=False, null=False)
    razorpay_signature = models.CharField(
        _('Razorpay signature'), max_length=150,
        blank=False, null=False)
    product_type = models.CharField(
        _('Product type'),
        max_length=1,
        choices=ProductTypes.PRODUCT_TYPE_IN_PRODUCT_TYPES,
        default=ProductTypes.NOT_SELECTED,
        blank=True)
    institute_common_license_order_details = models.ForeignKey(
        InstituteCommonLicenseOrderDetails,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='institute_license_order_details')


class RazorpayWebHookCallback(models.Model):
    """Stores Razorpay webhook callback credentials"""
    order_id = models.CharField(
        _('Razorpay order id'), max_length=100,
        blank=False, null=False)
    razorpay_payment_id = models.CharField(
        _('Razorpay payment id'), max_length=100,
        blank=False, null=False)
    product_type = models.CharField(
        _('Product type'),
        max_length=1,
        choices=ProductTypes.PRODUCT_TYPE_IN_PRODUCT_TYPES,
        default=ProductTypes.NOT_SELECTED,
        blank=True)


class ProfilePictures(models.Model):
    """Creates profile pictures model to store profile pictures"""
    user = models.ForeignKey(
        'User', related_name='profile_pictures', on_delete=models.CASCADE)
    image = models.ImageField(
        _('Image'),
        upload_to=user_profile_picture_upload_file_path,
        null=True,
        blank=True,
        max_length=1024,
        validators=(validate_image_file_extension,)
    )
    uploaded_on = models.DateTimeField(_('Uploaded on'),
                                       default=timezone.now, editable=False)
    class_profile_picture = models.BooleanField(
        _("ClassProfilePicture"), default=False)
    public_profile_picture = models.BooleanField(
        _("PublicProfilePicture"), default=False)

    class Meta:
        verbose_name_plural = 'Profile Pictures'

    def __str__(self):
        return str(self.image)


class Institute(models.Model):
    """Creates institute model where only teacher can create institute"""
    user = models.ForeignKey(
        'User', related_name='institutes', on_delete=models.CASCADE)
    name = models.CharField(
        _('Institute Name'), max_length=150, blank=False, null=False,
        validators=(MinLengthValidator(5), ProhibitNullCharactersValidator))
    country = CountryField(
        _('Country'), countries=OperationalCountries, default='IN')
    institute_category = models.CharField(
        _('Institute Category'), max_length=1,
        choices=InstituteCategory.CATEGORY_IN_INSTITUTE_CATEGORIES,
        blank=False, null=False)
    type = models.CharField(
        _('Institute Type'), max_length=2,
        choices=InstituteType.TYPE_IN_INSTITUTE_TYPE,
        blank=False, null=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False
    )
    institute_slug = models.SlugField(
        _('Institute Slug'),
        max_length=180,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        """Overriding save method"""
        if self.name:
            self.name = self.name.lower().strip()

        if not self.name:
            raise ValueError({'name': _('This field is required.')})

        if not self.type:
            raise ValueError({'type': _('This field is required.')})

        # Only teachers can create institute
        if not User.objects.get(email=self.user).is_teacher:
            raise PermissionDenied()

        super(Institute, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        """String representation"""
        return self.name.lower()

    def get_absolute_url(self):
        """Returns absolute url of the institute"""
        return reverse("institute:detail",
                       kwargs={'institute_slug': self.institute_slug})


@receiver(pre_save, sender=Institute)
def institute_slug_generator(sender, instance, *args, **kwargs):
    """Generates slug for institute"""
    if not instance.institute_slug:
        slug = unique_slug_generator_for_institute(instance)
        instance.institute_slug = slug


class InstituteProfile(models.Model):
    """Profile for institute"""
    institute = models.OneToOneField(
        'Institute',
        related_name='institute_profile',
        on_delete=models.CASCADE
    )
    motto = models.TextField(
        _('Motto'), max_length=256, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    phone = PhoneNumberField(_('Phone'), blank=True)
    website_url = models.URLField(_('Website Url'), blank=True)
    state = models.CharField(
        _('State'),
        max_length=2,
        choices=StatesAndUnionTerritories.STATE_IN_STATE_CHOICES,
        blank=True)
    pin = models.CharField(_('Pin Code'), max_length=10, blank=True)
    address = models.TextField(_('Address'), max_length=50, blank=True)
    recognition = models.CharField(
        _('Recognition'), max_length=30, blank=True)
    primary_language = models.CharField(
        _('Primary Language'), max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES, default='EN')
    secondary_language = models.CharField(
        _('Secondary Language'), max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES, blank=True)
    tertiary_language = models.CharField(
        _('Tertiary Language'), max_length=3,
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES, blank=True)

    def __str__(self):
        """String representation"""
        return str(self.institute)


class InstituteLogo(models.Model):
    """Creates logo model to store institute logos"""
    institute = models.ForeignKey(
        'Institute', related_name='institute_logo', on_delete=models.CASCADE)
    image = models.ImageField(
        _('Logo'),
        upload_to=institute_logo_upload_file_path,
        null=True,
        blank=True,
        max_length=1024,
        validators=(validate_image_file_extension,)
    )
    uploaded_on = models.DateTimeField(_('Uploaded on'),
                                       default=timezone.now, editable=False)
    active = models.BooleanField(_("Active"), default=False)

    class Meta:
        verbose_name_plural = 'Institute Logos'

    def __str__(self):
        return str(self.image)


class InstituteBanner(models.Model):
    """Creates banner model to store institute banners"""
    institute = models.ForeignKey(
        'Institute', related_name='institute_banner', on_delete=models.CASCADE)
    image = models.ImageField(
        _('Banner'),
        upload_to=institute_banner_upload_file_path,
        null=True,
        blank=True,
        max_length=1024,
        validators=(validate_image_file_extension,)
    )
    uploaded_on = models.DateTimeField(_('Uploaded on'),
                                       default=timezone.now, editable=False)
    active = models.BooleanField(_("Active"), default=False)

    class Meta:
        verbose_name_plural = 'Institute Banners'

    def __str__(self):
        return str(self.image)


class InstitutePermission(models.Model):
    """Creates Institute permissions model"""
    institute = models.ForeignKey(
        'Institute', related_name='permissions', on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        'User', related_name='invites', on_delete=models.SET_NULL,
        null=True)
    invitee = models.ForeignKey(
        'User', related_name='requests', on_delete=models.CASCADE)
    role = models.CharField(
        _('Permission'),
        choices=InstituteRole.ROLE_IN_INSTITUTE_ROLES,
        max_length=1,
        null=False,
        blank=False)
    active = models.BooleanField(_('Active'), default=False)
    request_date = models.DateTimeField(
        _('Request Date'), default=timezone.now, editable=False)
    request_accepted_on = models.DateTimeField(
        _('Request Accept Date'), null=True, blank=True)

    class Meta:
        unique_together = ('institute', 'invitee')

    def __str__(self):
        return str(self.invitee)


class InstituteStatistics(models.Model):
    """Creates model for storing institute statistics"""
    institute = models.OneToOneField(
        'Institute', related_name='institute_statistics',
        on_delete=models.CASCADE)
    no_of_admins = models.PositiveSmallIntegerField(_('No of Admins'), default=1)
    no_of_staffs = models.PositiveSmallIntegerField(_('No of Staffs'), default=0)
    no_of_faculties = models.PositiveSmallIntegerField(_('No of Faculties'), default=0)
    no_of_students = models.PositiveSmallIntegerField(_('No of Students'), default=0)
    department_count = models.PositiveSmallIntegerField(_('Department Count'), default=0)
    class_count = models.PositiveSmallIntegerField(_('Class Count'), default=0)
    section_count = models.PositiveSmallIntegerField(_('Section Count'), default=0)
    storage = models.DecimalField(_('Storage in Gb'), default=0.0,
                                  max_digits=14, decimal_places=9)
    uploaded_video_duration = models.PositiveIntegerField(
        _('Uploaded video duration in seconds'), default=0)
    uploaded_pdf_duration = models.PositiveIntegerField(
        _('Uploaded pdf reading duration in seconds'), default=0)

    def __str__(self):
        return self.institute.name


@receiver(post_save, sender=Institute)
def institute_is_created(sender, instance, created, **kwargs):
    if created:
        InstituteProfile.objects.create(institute=instance)
        admin_role = InstitutePermission.objects.create(
            institute=instance,
            inviter=instance.user,
            invitee=instance.user,
            role=InstituteRole.ADMIN,
            request_accepted_on=timezone.now(),
        )
        admin_role.active = True
        admin_role.save()
        InstituteStatistics.objects.create(institute=instance)
        InstituteLicenseStat.objects.create(institute=instance)
    else:
        try:
            instance.institute_profile.save()
        except ObjectDoesNotExist:
            InstituteProfile.objects.create(institute=instance)


class InstituteClass(models.Model):
    """Creates model to store institute classes"""
    class_institute = models.ForeignKey(
        'Institute', related_name='class_institute',
        on_delete=models.CASCADE)
    name = models.CharField(
        _('Name'), max_length=40, blank=False, null=False)
    class_slug = models.CharField(
        _('Class slug'), max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    class Meta:
        unique_together = ('class_institute', 'name')

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower().strip()

        if not self.name:
            raise ValueError(_('Name is required.'))

        super(InstituteClass, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=InstituteClass)
def institute_class_slug_generator(sender, instance, *args, **kwargs):
    """Generates slug for institute class"""
    if not instance.class_slug:
        slug = unique_slug_generator_for_class(instance)
        instance.class_slug = slug


class InstituteSubject(models.Model):
    """Creates model to store institute subject"""
    subject_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='subject_class')
    name = models.CharField(
        _('Subject Name'), max_length=50, blank=False, null=False)
    type = models.CharField(
        _('Subject Type'),
        max_length=1,
        choices=InstituteSubjectType.SUBJECT_TYPE_IN_INSTITUTE_SUBJECTS,
        blank=False,
        null=False)
    subject_slug = models.CharField(
        _('Subject Slug'), max_length=60, blank=True, null=False, unique=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()

        if not self.name:
            raise ValueError({'error': _('Subject name can not be blank.')})

        if not self.type:
            raise ValueError({'error': _('Subject type is required.')})

        super(InstituteSubject, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_class', 'name')

    def __str__(self):
        return self.name


@receiver(pre_save, sender=InstituteSubject)
def add_subject_slug(instance, *args, **kwargs):
    if not instance.subject_slug:
        instance.subject_slug = unique_slug_generator_for_subject(instance)


@receiver(post_save, sender=InstituteSubject)
def create_institute_subject_statistics_instance(sender, instance, created, *args, **kwargs):
    if created:
        InstituteSubjectStatistics.objects.create(
            statistics_subject=instance)
        SubjectViewNames.objects.create(
            view_subject=instance,
            key='MI',
            name='Meet Your Instructor')
        SubjectViewNames.objects.create(
            view_subject=instance,
            key='CO',
            name='Course Overview')
        SubjectViewNames.objects.create(
            view_subject=instance,
            key='M1',
            name='Module 1')

        if instance.type == InstituteSubjectType.MANDATORY:
            for invite in InstituteClassStudents.objects.filter(
                institute_class__pk=instance.subject_class.pk
            ).only('institute_student'):
                InstituteSubjectStudents.objects.create(
                    institute_subject=instance,
                    institute_student=invite.institute_student,
                    inviter=invite.inviter,
                    active=invite.active
                )


class SubjectBookmarked(models.Model):
    """Stores bookmarked subject by student"""
    subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='bookmarked_subject')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subject_bookmarking_user')

    class Meta:
        unique_together = ('subject', 'user')

    def __str__(self):
        return str(self.user)


class InstituteSubjectStatistics(models.Model):
    """Stores Institute Subject Statistics"""
    statistics_subject = models.OneToOneField(
        InstituteSubject, on_delete=models.CASCADE, related_name='statistics_subject')
    storage = models.DecimalField(
        _('Storage used'), max_digits=14, decimal_places=9, default=0.0, blank=True)
    uploaded_video_duration = models.PositiveIntegerField(
        _('Uploaded Video Duration in seconds'), default=0, blank=True)
    uploaded_pdf_duration = models.PositiveIntegerField(
        _('Uploaded Video Duration in seconds'), default=0, blank=True)


class InstituteSection(models.Model):
    """Creates model to store institute section"""
    section_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='section_class')
    name = models.CharField(
        _('Section Name'), max_length=20, blank=False, null=False)
    section_slug = models.CharField(
        _('Section Slug'), max_length=32, blank=True, null=False, unique=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()

        if not self.name:
            raise ValueError({'error': _('Section name can not be blank.')})

        super(InstituteSection, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('section_class', 'name')

    def __str__(self):
        return self.name


@receiver(pre_save, sender=InstituteSection)
def add_section_slug(instance, *args, **kwargs):
    if not instance.section_slug:
        instance.section_slug = unique_slug_generator_for_section(instance)


class InstituteClassPermission(models.Model):
    """Model to store staff/admin assigned to class by admin"""
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='perm_class_invitee')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='perm_class_inviter')
    to = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE,
        related_name='perm_class_institute')
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    def __str__(self):
        return str(self.invitee)

    class Meta:
        unique_together = ('to', 'invitee')


class InstituteSubjectPermission(models.Model):
    """Model to store staff/admin/faculty assigned to class by admin/staff"""
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='perm_subject_invitee')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='perm_subject_inviter')
    to = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE,
        related_name='perm_subject_institute')
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    def __str__(self):
        return str(self.invitee)

    class Meta:
        unique_together = ('to', 'invitee')


class InstituteSectionPermission(models.Model):
    """Model to store staff/admin assigned to section by admin"""
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='perm_section_invitee')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='perm_section_inviter')
    to = models.ForeignKey(
        InstituteSection, on_delete=models.CASCADE,
        related_name='perm_section_institute')
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, editable=False)

    def __str__(self):
        return str(self.invitee)

    class Meta:
        unique_together = ('to', 'invitee')


class SubjectViewNames(models.Model):
    """For storing view name of subjects"""
    view_subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='view_subject')
    key = models.CharField(_('Key'), max_length=6, blank=False)
    name = models.CharField(_('Name'), max_length=30, blank=False)
    order = models.PositiveIntegerField(_('Order'), blank=True, null=True)
    type = models.CharField(
        _('View Type'),
        max_length=1,
        choices=SubjectViewType.VIEW_TYPE_IN_VIEW_TYPES,
        default=SubjectViewType.MODULE_VIEW,
        blank=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValueError(_('Name is required and can not be blank.'))
        self.key = self.key.upper()
        super(SubjectViewNames, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['view_subject', 'key'], name='unique_key_for_subject_constraint')
        ]


@receiver(pre_save, sender=SubjectViewNames)
def set_view_key(instance, *args, **kwargs):
    if not instance.key:
        instance.key = unique_key_generator_for_subject_view_name(instance.view_subject)


@receiver(post_save, sender=SubjectViewNames)
def set_order_automatically(sender, instance, created, *args, **kwargs):
    if created:
        instance.order = instance.pk
        instance.save()


class SubjectIntroductoryContent(models.Model):
    """Model for storing subject meet your instructor and course overview"""
    view = models.ForeignKey(
        SubjectViewNames, on_delete=models.CASCADE, related_name="introductory_content_view")
    name = models.CharField(
        _('Content name'), max_length=30, blank=False, null=False)
    file = models.FileField(
        _('File'),
        upload_to=subject_introductory_content_upload_file_path,
        null=True,
        blank=True,
        max_length=1024)
    can_download = models.BooleanField(_('Can Download'), blank=True, default=False)
    link = models.URLField(
        _('Link'), max_length=2083, blank=True, null=True)
    content_type = models.CharField(
        _('Content Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=SubjectIntroductionContentType.CONTENT_TYPE_IN_CONTENT_TYPES)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.can_download:
            self.can_download = False
        super(SubjectIntroductoryContent, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubjectModuleView(models.Model):
    """Model for storing subject module views"""
    view = models.ForeignKey(
        SubjectViewNames, on_delete=models.CASCADE, related_name="lecture_view")
    type = models.CharField(
        _('Lecture View Type'),
        max_length=1,
        choices=SubjectModuleViewType.VIEW_TYPE_IN_VIEW_TYPES)
    lecture = models.ForeignKey(
        'SubjectLecture', on_delete=models.CASCADE, related_name="view_subject_lecture",
        blank=True, null=True)
    test = models.ForeignKey(
        'SubjectTest', on_delete=models.CASCADE, related_name="view_test",
        blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.type == SubjectModuleViewType.LECTURE_VIEW:
            if not self.lecture:
                raise ValueError(_('PROGRAMMING ERROR: Subject lecture is required.'))
        elif self.type == SubjectModuleViewType.TEST_VIEW:
            if not self.test:
                raise ValueError(_('PROGRAMMING ERROR: Subject test is required.'))
        super(SubjectModuleView, self).save(*args, **kwargs)

    def __str__(self):
        return self.type


class SubjectLecture(models.Model):
    """Model for storing subject lecture names"""
    name = models.CharField(
        _('Lecture name'), max_length=30, blank=False, null=False)
    target_date = models.DateField(
        _('Target Date'), max_length=10, blank=True, null=True)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super(SubjectLecture, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubjectAdditionalReadingUseCaseLink(models.Model):
    """Model for storing additional reading and use case link"""
    lecture = models.ForeignKey(SubjectLecture, on_delete=models.CASCADE, related_name="lecture_links")
    name = models.CharField(_('Name of Link'), max_length=100, blank=False, null=False)
    link = models.URLField(_('Link'), max_length=2083, blank=False, null=False)
    type = models.CharField(
        _('Link View Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=SubjectAdditionalReadingOrUseCaseLinkType.LINK_VIEW_TYPE_IN_LINK_VIEW_TYPES)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValueError(_('Name is required and can not be blank.'))
        if not self.link:
            raise ValueError(_('Link is required.'))
        super(SubjectAdditionalReadingUseCaseLink, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubjectLectureMaterials(models.Model):
    """Model for storing lecture materials"""
    lecture = models.ForeignKey(
        SubjectLecture, on_delete=models.CASCADE, related_name="lecture_material")
    content_type = models.CharField(
        _('Content Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=SubjectLectureMaterialsContentType.CONTENT_TYPE_IN_CONTENT_TYPES)
    name = models.CharField(
        _('Name of study material'), max_length=100, blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValueError(_('Name of material is required and can not be blank.'))
        super(SubjectLectureMaterials, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubjectLectureImageMaterial(models.Model):
    """Model for storing image study material of subject lecture"""
    lecture_material = models.ForeignKey(
        SubjectLectureMaterials, on_delete=models.CASCADE, related_name="image_lecture_material")
    file = models.FileField(
        _('Image File'),
        upload_to=subject_img_study_material_upload_file_path,
        null=False,
        blank=False,
        max_length=1024,
        unique=True)
    can_download = models.BooleanField(_('Can Download'), blank=True, default=True)

    def __str__(self):
        return str(self.lecture_material)


@receiver(post_delete, sender=SubjectLectureImageMaterial)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
            except Exception as e:
                print('Error: ' + e)


class SubjectLecturePdfMaterial(models.Model):
    """Model for storing pdf study material of subject lecture"""
    lecture_material = models.ForeignKey(
        SubjectLectureMaterials, on_delete=models.CASCADE, related_name="pdf_lecture_material")
    file = models.FileField(
        _('Pdf File'),
        upload_to=subject_pdf_study_material_upload_file_path,
        null=False,
        blank=False,
        max_length=1024,
        unique=True)
    can_download = models.BooleanField(_('Can Download'), blank=True, default=True)

    def __str__(self):
        return str(self.lecture_material)


@receiver(post_delete, sender=SubjectLecturePdfMaterial)
def auto_delete_pdf_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
            except Exception as e:
                print('Error: ' + e)


class SubjectLectureLinkMaterial(models.Model):
    """Model for storing link study material of subject lecture"""
    lecture_material = models.ForeignKey(
        SubjectLectureMaterials, on_delete=models.CASCADE, related_name="link_lecture_material")
    link = models.URLField(
        _('Link'), max_length=2083, blank=False, null=False)

    def __str__(self):
        return str(self.lecture_material)


class SubjectLectureLiveClass(models.Model):
    """Model for storing live class schedule of subject lecture"""
    lecture_material = models.ForeignKey(
        SubjectLectureMaterials, on_delete=models.CASCADE, related_name="live_class_lecture_material")
    live_on = models.DateTimeField(
        _('Live schedule'), blank=False, null=False)
    link = models.URLField(
        _('Live Link'), max_length=2048, blank=False, null=False)

    def __str__(self):
        return str(self.lecture_material)


class SubjectLectureUseCaseObjectives(models.Model):
    """Models for storing use cases and objectives of subject lecture."""
    lecture = models.ForeignKey(
        SubjectLecture, on_delete=models.CASCADE, related_name="lecture_use_cases")
    text = models.CharField(
        _('Text'), max_length=500, blank=False, null=False)
    type = models.CharField(
        _('Text Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=SubjectLectureUseCaseOrObjectives.VIEW_TYPE_IN_VIEW_TYPES)

    def save(self, *args, **kwargs):
        if self.text:
            self.text = self.text.strip()
        if not self.text:
            raise ValueError(_('Text can not be blank.'))
        super(SubjectLectureUseCaseObjectives, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.lecture)


class SubjectLectureAssignment(models.Model):
    """Models for storing assignment question of subject lecture."""
    lecture_material = models.ForeignKey(
        SubjectLectureMaterials, on_delete=models.CASCADE, related_name="lecture_assignment")
    question = models.CharField(
        _('Lecture Question'), max_length=500, blank=False, null=False)
    description = models.CharField(
        _('Lecture Description'), max_length=1000, blank=False, null=False)
    due_date = models.DateField(
        _('Due Date'), max_length=10, blank=True, default='')
    assignment_type = models.CharField(
        _('Assignment Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=SubjectAssignmentType.ASSIGNMENT_TYPE_IN_SUBJECT_ASSIGNMENT_TYPES)
    graded_type = models.CharField(
        _('Graded Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=GradedType.GRADED_TYPE_IN_GRADED_TYPES)
    total_mark = models.DecimalField(
        _('Total Mark'), default=0.0, max_digits=6, decimal_places=2, blank=True)


class InstituteSubjectCourseContentQuestions(models.Model):
    """Model for storing subject course content questions"""
    # course_content = models.ForeignKey(
    #     InstituteSubjectCourseContent, on_delete=models.CASCADE, related_name='course_content')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='question_user', blank=False, null=True)
    anonymous = models.BooleanField(
        _('Anonymous'), default=False, blank=True)
    question = models.CharField(
        _('Question'), max_length=256, blank=False, null=False)
    edited = models.BooleanField(
        _('Question Edited'), default=False, blank=True)
    description = models.CharField(
        _('Description'), max_length=2000, blank=True, default='')
    rgb_color = models.CharField(
        _('RGB color'), max_length=26, blank=False, null=False)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.question:
            raise ValueError('Question field is required.')
        if not self.rgb_color:
            raise ValueError('RGB color field is required.')
        if self.description:
            self.description = self.description.strip()
        self.question = self.question.strip()
        super(InstituteSubjectCourseContentQuestions, self).save(*args, **kwargs)

    def __str__(self):
        return self.question.lower()

    # class Meta:
    #     unique_together = ('course_content', 'question')


class InstituteSubjectCourseContentAnswer(models.Model):
    """Model for storing institute subject course content answer"""
    content_question = models.ForeignKey(
        InstituteSubjectCourseContentQuestions, on_delete=models.CASCADE, related_name='content_question')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='answer_user', blank=False, null=True)
    anonymous = models.BooleanField(
        _('Anonymous'), default=False, blank=True)
    answer = models.CharField(
        _('Answer'), max_length=2000, blank=False, null=False)
    edited = models.BooleanField(
        _('Answer Edited'), default=False, blank=True)
    rgb_color = models.CharField(
        _('RGB color'), max_length=26, blank=False, null=False)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)
    pin = models.BooleanField(
        _('Pinned answer'), default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.answer:
            raise ValueError('Answer field is required.')
        if not self.rgb_color:
            raise ValueError('RGB color field is required.')
        self.answer = self.answer.strip()
        super(InstituteSubjectCourseContentAnswer, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.content_question)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_question', 'answer'],
                name='unique_answer_constraint'
            ),
            models.UniqueConstraint(
                fields=['content_question', 'pin'],
                condition=Q(pin=True),
                name='unique_pinned_answer_constraint'
            ),
        ]


class InstituteSubjectCourseContentQuestionUpvote(models.Model):
    """Model for storing the upvote of questions"""
    course_content_question = models.ForeignKey(
        InstituteSubjectCourseContentQuestions, on_delete=models.CASCADE,
        related_name='course_content_question')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='question_upvote_user')

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('course_content_question', 'user')


class InstituteSubjectCourseContentAnswerUpvote(models.Model):
    """Model for storing the upvote of answers"""
    course_content_answer = models.ForeignKey(
        InstituteSubjectCourseContentAnswer, on_delete=models.CASCADE,
        related_name='course_content_answer')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answer_upvote_user')

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('course_content_answer', 'user')


class InstituteStudents(models.Model):
    """Model for storing student in institute"""
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_student_user')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='institute_student_inviter', null=True)
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='institute_student_institute')
    enrollment_no = models.CharField(
        _('Enrollment no'), max_length=15, blank=True, default='')
    registration_no = models.CharField(
        _('Registration no'), max_length=15, blank=True, default='')
    first_name = models.CharField(
        _('First name'), max_length=30, blank=True, default='')
    last_name = models.CharField(
        _('Last name'), max_length=30, blank=True, default='')
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        blank=True,
        default=Gender.NOT_MENTIONED,
        choices=Gender.GENDER_IN_GENDER_CHOICES)
    date_of_birth = models.DateField(
        _('Date of Birth'), max_length=10, null=True, blank=True)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)
    edited = models.BooleanField(
        _('Edited'), default=False, blank=True)   # For allowing invitee to change first name last name only once.
    active = models.BooleanField(
        _('Active'), default=False, blank=True)
    is_banned = models.BooleanField(
        _('Is Banned'), default=False, blank=True)

    def save(self, *args, **kwargs):
        if self.enrollment_no:
            self.enrollment_no = self.enrollment_no.strip()
        if self.registration_no:
            self.registration_no = self.registration_no.strip()
        if self.first_name:
            self.first_name = self.first_name.lower().strip()
        if self.last_name:
            self.last_name = self.last_name.lower().strip()
        super(InstituteStudents, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.invitee)

    class Meta:
        unique_together = ('invitee', 'institute')


class InstituteClassStudents(models.Model):
    """Model for storing institute class students"""
    institute_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='student_institute_class')
    institute_student = models.OneToOneField(
        InstituteStudents, on_delete=models.CASCADE, related_name='class_student_institute_profile')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='class_student_inviter', null=True)
    active = models.BooleanField(_('Active'), default=False, blank=True)
    is_banned = models.BooleanField(_('Is Banned'), default=False, blank=True)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)

    def __str__(self):
        return str(self.institute_student.invitee)

    class Meta:
        unique_together = ('institute_student', 'institute_class')


@receiver(post_save, sender=InstituteClassStudents)
def add_student_to_subject(sender, instance, created, *args, **kwargs):
    if created:
        for subject in InstituteSubject.objects.filter(
            subject_class__pk=instance.institute_class.pk,
            type=InstituteSubjectType.MANDATORY
        ):
            InstituteSubjectStudents.objects.create(
                institute_subject=subject,
                institute_student=instance.institute_student,
                inviter=instance.inviter,
                active=instance.active
            )


class InstituteSubjectStudents(models.Model):
    """Model for storing institute subject students"""
    institute_subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='student_institute_subject')
    institute_student = models.OneToOneField(
        InstituteStudents, on_delete=models.CASCADE, related_name='subject_student_institute_profile')
    inviter = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='subject_student_inviter', null=True)
    active = models.BooleanField(_('Active'), default=False, blank=True)
    is_banned = models.BooleanField(_('Is Banned'), default=False, blank=True)
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)

    def __str__(self):
        return str(self.institute_student.invitee)

    class Meta:
        unique_together = ('institute_student', 'institute_subject')


class InstituteStudyMaterialPreviewStats(models.Model):
    """Model for storing institute study material preview statistics"""
    # course_content = models.ForeignKey(
    #     InstituteSubjectCourseContent, on_delete=models.CASCADE, related_name='institute_course_content')
    completed = models.BooleanField('Completed', default=False, blank=True)
    completed_on = models.DateTimeField(
        _('Completed On'), default=timezone.now, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='course_content_user')

    def __str__(self):
        return str(self.user)

    # class Meta:
    #     unique_together = ('user', 'course_content')


class InstituteBannedStudent(models.Model):
    """Model to store banned student from institute"""
    institute_student = models.ForeignKey(
        InstituteStudents, on_delete=models.CASCADE, related_name='institute_banned_student')
    banned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_banning_user')
    banned_institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='banned_institute')
    start_date = models.DateTimeField(
        _('Start Date'), blank=False, null=False)
    end_date = models.DateTimeField(
        _('End Date'), blank=True, null=True)
    reason = models.CharField(
        _('Reason'), max_length=100, blank=False, null=False)
    active = models.BooleanField(
        _('Ban Active'), default=True, blank=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.reason:
            raise ValueError(_('You need to provide a reason for banning.'))
        self.reason = self.reason.strip()
        super(InstituteBannedStudent, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.institute_student.invitee)


class InstituteClassBannedStudent(models.Model):
    """Model to store banned student from class"""
    institute_student = models.ForeignKey(
        InstituteStudents, on_delete=models.CASCADE, related_name='class_banned_student')
    banned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='class_banned_by')
    banned_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='banned_class')
    start_date = models.DateTimeField(
        _('Start Date'), blank=False, null=False)
    end_date = models.DateTimeField(
        _('End Date'), blank=True, null=True)
    reason = models.CharField(
        _('Reason'), max_length=500, blank=False, null=False)
    active = models.BooleanField(
        _('Ban Active'), default=True, blank=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.reason:
            raise ValueError(_('You need to provide a reason for banning.'))
        self.reason = self.reason.strip()
        super(InstituteClassBannedStudent, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.institute_student.invitee)


class InstituteSubjectBannedStudent(models.Model):
    """Model to store banned student from subject"""
    institute_student = models.ForeignKey(
        InstituteStudents, on_delete=models.CASCADE, related_name='subject_banned_student')
    banned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subject_banned_by')
    banned_subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='banned_subject')
    start_date = models.DateTimeField(
        _('Start Date'), blank=False, null=False)
    end_date = models.DateTimeField(
        _('End Date'), blank=True, null=True)
    reason = models.CharField(
        _('Reason'), max_length=100, blank=False, null=False)
    active = models.BooleanField(
        _('Ban Active'), default=True, blank=True)
    created_on = models.DateTimeField(
        _('Created On'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.reason:
            raise ValueError(_('You need to provide a reason for banning.'))
        self.reason = self.reason.strip()
        super(InstituteSubjectBannedStudent, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.institute_student.invitee)


class InstituteLastSeen(models.Model):
    """Model to store last seen in institute"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_last_seen_user')
    last_seen_institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='last_seen_institute')
    last_seen = models.DateTimeField(
        _('Last Seen'), default=timezone.now, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('user', 'last_seen_institute')


class InstituteClassLastSeen(models.Model):
    """Model to store last seen in institute class"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_class_last_seen_user')
    last_seen_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='last_seen_class')
    last_seen = models.DateTimeField(
        _('Last Seen'), default=timezone.now, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('user', 'last_seen_class')


class InstituteSubjectLastSeen(models.Model):
    """Model to store last seen in institute subject"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_subject_last_seen_user')
    last_seen_subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='last_seen_subject')
    last_seen = models.DateTimeField(
        _('Last Seen'), default=timezone.now, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('user', 'last_seen_subject')


#####################################################################
# Models for digital adaptive test
# Models for creating Question paper
#####################################################################
class SubjectTest(models.Model):
    """Model to create test"""
    subject = models.ForeignKey(
        InstituteSubject, on_delete=models.CASCADE, related_name='test_subject')
    lecture = models.ForeignKey(
        SubjectLecture, on_delete=models.CASCADE,
        related_name='test_lecture', blank=True, null=True)
    view = models.ForeignKey(
        SubjectViewNames, on_delete=models.CASCADE,
        related_name='test_view', null=True, blank=True)
    test_place = models.CharField(
        'Test place view',
        max_length=1,
        choices=TestPlace.PLACES_IN_PLACE_TYPES)
    name = models.CharField(_('Test Name'), max_length=30, null=False)
    type = models.CharField(
        _('Test Type'),
        max_length=1,
        choices=GradedType.GRADED_TYPE_IN_GRADED_TYPES)
    total_marks = models.DecimalField(
        _('Total Marks'), decimal_places=2, max_digits=7)
    total_duration = models.PositiveSmallIntegerField(
        _('Total Duration in minutes'))
    test_schedule_type = models.CharField(
        _('Test schedule type'),
        max_length=2,
        choices=TestScheduleType.TYPE_IN_TEST_SCHEDULE_TYPES)
    test_schedule = UnixTimeStampField(
        _('Test schedule in UNIX timestamp in millisecond'), use_numeric=True, blank=True, null=True)
    instruction = models.CharField(
        _('Instruction'), max_length=200, blank=True, default='')
    no_of_optional_section_answer = models.PositiveSmallIntegerField(
        _('Number of optional section answer'), default=0, blank=True)
    question_mode = models.CharField(
        _('Question Mode'),
        max_length=1,
        choices=QuestionMode.QUESTION_MODE_IN_QUESTION_MODES)
    answer_mode = models.CharField(
        _('Answer Mode'),
        max_length=1,
        choices=AnswerMode.ANSWER_MODE_IN_ANSWER_MODES)
    question_category = models.CharField(
        _('Question Category'),
        max_length=1,
        choices=QuestionCategory.QUESTION_CATEGORY_IN_QUESTION_CATEGORIES)
    no_of_attempts = models.PositiveSmallIntegerField(
        _('No of attempts to take exam'), default=0, blank=True)
    publish_result_automatically = models.BooleanField(_('Publish result automatically'))
    enable_peer_check = models.BooleanField(_('Enable peer check'))
    allow_question_preview_10_min_before = models.BooleanField(_('Allow question preview 10 min before'))
    shuffle_questions = models.BooleanField(_('Shuffle Questions'))
    result_published = models.BooleanField(_('Result Published'), default=False, blank=True)
    test_live = models.BooleanField(_('Test live'), blank=True, default=False)
    test_slug = models.CharField(_('Test Slug'), max_length=10, blank=True, null=False)
    created_on = models.DateTimeField(_('Created on'), default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError(_('Test name is required.'))

        if int(self.total_duration) < 1:
            raise ValueError(_('Total duration should be a positive integer.'))

        if float(self.total_marks) <= 0.0:
            raise ValueError(_('Total marks should be a > 0.'))

        if self.no_of_optional_section_answer < 0:
            raise ValueError(_('No of optional section answer should be a positive integer.'))

        if self.question_mode == QuestionMode.TYPED or self.question_mode == QuestionMode.IMAGE:
            if self.answer_mode == AnswerMode.FILE:
                raise ValueError(_('Answer mode should be TYPED if question mode is TYPED or IMAGE.'))

            if self.question_category == QuestionCategory.FILE_UPLOAD_TYPE:
                raise ValueError(_('Question category can not be FILE UPLOAD TYPE if question mode is TYPED or IMAGE.'))

        if self.question_category == QuestionCategory.AUTOCHECK_TYPE:
            if self.enable_peer_check:
                raise ValueError(_('Can not set test ENABLE PEER CHECK since question category is AUTOCHECK TYPE.'))

        if self.test_schedule_type == TestScheduleType.UNSCHEDULED:
            if self.allow_question_preview_10_min_before:
                msg = _('Can not set QUESTION PREVIEW 10 MINUTES BEFORE since selected test type is UNSCHEDULED.')
                raise ValueError(msg)

        if self.type == GradedType.GRADED:
            if int(self.no_of_attempts) > 1:
                msg = _('For Graded test number of attempts can not be greater than 1.')
                raise ValueError(msg)

        if self.test_schedule:
            current_time = int(time.time()) * 1000  # In milliseconds

            if current_time > self.test_schedule:
                raise ValueError(_('Test can not be scheduled in the past.'))

        if self.instruction:
            self.instruction = self.instruction.strip()

        super(SubjectTest, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=SubjectTest)
def create_test_slug(sender, instance, *args, **kwargs):
    if not instance.test_slug:
        instance.test_slug = generate_test_slug(instance)


class SubjectTestSets(models.Model):
    """Model for creating multiple test set"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='test_set_test')
    set_name = models.CharField(
        _('Set Name'), max_length=20, blank=False, null=False)
    set_slug = models.CharField(
        _('Set Slug'), max_length=8, blank=False, null=False)
    verified = models.BooleanField(
        _('Set Verified'), default=False, blank=True)
    active = models.BooleanField(
        _('Set Active'), default=False, blank=True)


@receiver(pre_save, sender=SubjectTestSets)
def set_test_slug(instance, *args, **kwargs):
    if not instance.set_slug:
        instance.set_slug = unique_slug_generator_for_test_set(instance)


class SubjectTestConceptLabels(models.Model):    # If answer mode is typed
    """Model for creating concept labels"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='test_concept_labels')
    name = models.CharField(
        _('Name'), max_length=30, blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip()

        super(SubjectTestConceptLabels, self).save(*args, **kwargs)


class SubjectFileTestQuestion(models.Model):   # If question mode is file
    """Model for storing test file question"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='file_question_test')
    set = models.ForeignKey(
        SubjectTestSets, on_delete=models.CASCADE, related_name='file_question_set')
    file = models.FileField(
        _('File'),
        upload_to=subject_file_test_question_file_path,
        null=True,
        blank=True,
        max_length=1024)


class SubjectTestQuestionSection(models.Model):    # If question mode is typed / image
    """Model for storing question section"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='question_section_test')
    set = models.ForeignKey(
        SubjectTestSets, on_delete=models.CASCADE, related_name='question_section_set')
    type = models.CharField(
        _('Section Type'),
        max_length=1,
        choices=TestQuestionSectionType.TYPE_IN_SECTION_TYPES)
    name = models.CharField(
        _('Name of question section'), max_length=100, blank=True, default='')
    order = models.PositiveIntegerField(
        _('Order'), blank=True, null=True)


@receiver(post_save, sender=SubjectTestQuestionSection)
def set_test_question_section_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.order = instance.pk
        instance.save()


class SubjectPictureTestQuestion(models.Model):           # If question mode is picture
    """Model for storing questions if question mode is picture"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='picture_question_test')
    test_section = models.ForeignKey(
        SubjectTestQuestionSection,
        on_delete=models.CASCADE,
        related_name='picture_question_section')
    order = models.PositiveIntegerField(
        _('Order'), blank=True, null=True)
    marks = models.DecimalField(
        _('Marks'), decimal_places=2, max_digits=5)
    file = models.FileField(
        _('File'),
        upload_to=subject_image_test_question_file_path,
        null=True,
        blank=True,
        max_length=1024)


@receiver(post_save, sender=SubjectPictureTestQuestion)
def set_picture_test_question_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.order = instance.pk
        instance.save()


class SubjectTypedTestQuestion(models.Model):
    """Model for storing typed test questions"""
    test_section = models.ForeignKey(
        SubjectTestQuestionSection, on_delete=models.CASCADE, related_name='typed_test_question_section')
    type = models.CharField(
        _('Question type'),
        max_length=1,
        choices=QuestionType.TYPE_IN_QUESTION_TYPES,
        blank=False)
    concept_label = models.ForeignKey(
        SubjectTestConceptLabels, on_delete=models.SET_NULL, blank=True, null=True)
    question = models.TextField(
        'Question', blank=True, default='')
    marks = models.DecimalField(
        'Marks', max_digits=5, decimal_places=2)
    order = models.PositiveIntegerField(
        _('Order'), blank=True, null=True)


@receiver(post_save, sender=SubjectTypedTestQuestion)
def set_typed_test_question_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.order = instance.pk
        instance.save()


class SubjectTestQuestionImage(models.Model):
    """Model for storing test question image"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='image_typed_test_question')
    file = models.FileField(
        _('File'),
        upload_to=subject_image_test_question_file_path,
        null=True,
        blank=True,
        max_length=1024)


class SubjectTestMcqOptions(models.Model):
    """Model for storing subject test mcq options and correct answer"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_mcq_question')
    option = models.CharField(
        _('Option'), max_length=200, blank=False)
    correct_answer = models.BooleanField(_('Is Correct Answer'))


class SubjectTestTrueFalseCorrectAnswer(models.Model):
    """Model for storing subject test True False correct answer"""
    question = models.OneToOneField(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_true_false_question')
    correct_answer = models.BooleanField(_('True / False correct answer'))


class SubjectTestSelectMultipleCorrectAnswer(models.Model):
    """Model for storing subject test select multiple correct answer"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_select_multiple_question')
    option = models.CharField(
        _('Option'), max_length=200, blank=False)
    correct_answer = models.BooleanField(_('Is Correct Answer'))


class SubjectTestNumericCorrectAnswer(models.Model):
    """Model for storing subject test numeric correct answer"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_numeric_question')
    correct_answer = models.DecimalField(
        _('Correct Answer'), max_digits=20, decimal_places=6)


class SubjectTestAssertionCorrectAnswer(models.Model):
    """Model for storing subject test assertion correct answer"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_assertion_answer')
    correct_answer = models.BooleanField(_('True / False correct answer'))


class SubjectTestFillInTheBlankCorrectAnswer(models.Model):
    """Model for storing subject fill in the blank correct answer"""
    question = models.ForeignKey(
        SubjectTypedTestQuestion, on_delete=models.CASCADE, related_name='typed_test_fill_in_the_blank_answer')
    correct_answer = models.CharField(
        _('Correct Answer'), max_length=100)
    enable_strict_checking = models.BooleanField(_('Enable strict checking.'), default=False)
    ignore_grammar = models.BooleanField(_('Ignore Grammar'), default=True)
    ignore_special_characters = models.BooleanField(_('Ignore Special Characters'), default=True)

    def save(self, *args, **kwargs):
        if self.enable_strict_checking and (self.ignore_grammar or self.ignore_special_characters):
            raise ValueError('Grammar and special characters can not be ignored if strict checking is enabled.')
        super(SubjectTestFillInTheBlankCorrectAnswer, self).save(*args, **kwargs)


#####################################################################
# Models for test credentials
#####################################################################
class StudentTestCredential(models.Model):
    """Model for storing test credentials"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='student_subject_test_credential')
    set = models.ForeignKey(
        SubjectTestSets, on_delete=models.CASCADE, related_name='student_test_question_set')
    student = models.ForeignKey(
        InstituteStudents, on_delete=models.CASCADE, related_name='student_test_credential')
    password = models.CharField(
        _('Test Password'), max_length=500, blank=True, null=False)
    no_of_warning = models.PositiveSmallIntegerField(
        _('Number of warnings'), default=0, blank=True)
    logged_in = models.BooleanField(
        _('Logged In'), default=False, blank=True)


@receiver(pre_save, sender=StudentTestCredential)
def create_password(instance, *args, **kwargs):
    if not instance.password:
        instance.password = generate_student_test_password(instance)


class StudentTestLoginStats(models.Model):
    """Model for storing login statistics of student"""
    test = models.ForeignKey(
        SubjectTest, on_delete=models.CASCADE, related_name='student_subject_test_login_stats')
    attempt = models.PositiveSmallIntegerField(_('Login Attempts'))
    net_speed = models.CharField('Net Speed', max_length=50, blank=True, null=True)
    login_state = models.CharField(
        _('Login State'),
        max_length=2,
        choices=StatesAndUnionTerritories.STATE_IN_STATE_CHOICES,
        blank=True,
        null=True)
    other_region = models.CharField(
        _('Other Region login'), max_length=100, blank=True, default='')
    login_country = CountryField(
        _('Login Country'), countries=OperationalCountries, default='IN')
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)
