import os
import datetime
import random
import string
import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import EmailValidator, MinLengthValidator, \
    ProhibitNullCharactersValidator, validate_image_file_extension
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from app import settings

from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token

from .tasks import create_welcome_message_after_user_creation

# Constant to define unlimited limit
UNLIMITED = 99999


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
    GENDER_IN_GENDER_CHOICES = [
        (MALE, _(u'Male')),
        (FEMALE, _(u'Female')),
        (OTHER, _(u'Other'))
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


class InstituteLicensePlans:
    BASIC = 'BAS'
    BUSINESS = 'BUS'
    ENTERPRISE = 'ENT'

    LICENSE_PLANS_IN_INSTITUTE_LICENSE = [
        (BASIC, _(u'BASIC')),
        (BUSINESS, _(u'BUSINESS')),
        (ENTERPRISE, _(u'ENTERPRISE'))
    ]


class DiscussionForumBar:
    ONE_PER_SUBJECT = 'O'
    ONE_PER_SUBJECT_OR_SECTION = 'S'

    DISCUSSION_FORUM_BAR_IN_DISCUSSION_FORUMS = [
        (ONE_PER_SUBJECT, _(u'ONE_PER_SUBJECT')),
        (ONE_PER_SUBJECT_OR_SECTION, _(u'ONE_PER_SUBJECT_OR_SECTION')),
    ]


class PaymentGateway:
    RAZORPAY = 'R'

    PAYMENT_GATEWAY_IN_PAYMENT_GATEWAYS = [
        (RAZORPAY, _(u'RAZORPAY')),
    ]


class StudyMaterialContentType:
    VIDEO = 'V'
    IMAGE = 'I'
    PDF = 'P'
    EXTERNAL_LINK = 'L'

    CONTENT_TYPE_IN_CONTENT_TYPES = [
        (VIDEO, _(u'VIDEO')),
        (IMAGE, _(u'IMAGE')),
        (PDF, _(u'PDF')),
        (EXTERNAL_LINK, _(u'EXTERNAL_LINK')),
    ]


class StudyMaterialView:
    MEET_YOUR_INSTRUCTOR = 'MI'
    COURSE_OVERVIEW = 'CO'

    STUDY_MATERIAL_VIEW_TYPES = [
        (MEET_YOUR_INSTRUCTOR, _(u'MEET_YOUR_INSTRUCTOR')),
        (COURSE_OVERVIEW, _(u'COURSE_OVERVIEW'))
    ]


class Weeks:
    NONE = 'NO'
    WEEK_1 = 'W1'
    WEEK_2 = 'W2'
    WEEK_3 = 'W3'
    WEEK_4 = 'W4'

    WEEK_IN_WEEK_TYPES = [
        (NONE, _(u'NONE')),
        (WEEK_1, _(u'WEEK_1')),
        (WEEK_2, _(u'WEEK_2')),
        (WEEK_3, _(u'WEEK_3')),
        (WEEK_4, _(u'WEEK_4')),
    ]


def user_profile_picture_upload_file_path(instance, filename):
    """Generates file path for uploading images in user profile"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'pictures/uploads/user/profile'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def institute_logo_upload_file_path(instance, filename):
    """Generates file path for uploading institute logo"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'pictures/uploads/institute/logo'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def institute_banner_upload_file_path(instance, filename):
    """Generates file path for uploading institute banner"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'pictures/uploads/institute/banner'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


def subject_img_study_material_upload_file_path(instance, filename):
    """Generates file path for uploading institute image study material"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'institute/uploads/content/image'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)
    return full_path


def subject_video_study_material_upload_file_path(instance, filename):
    """Generates file path for uploading institute video study material"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'institute/uploads/content/video'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)
    return full_path


def subject_pdf_study_material_upload_file_path(instance, filename):
    """Generates file path for uploading institute pdf study material"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'institute/uploads/content/pdf'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)
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
        # Creating teacher profile
        if instance.is_teacher:
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


class InstituteLicense(models.Model):
    """Creates institute license model to store pricing structure"""
    user = models.ForeignKey(
        'User', related_name='institute_licenses', on_delete=models.CASCADE)
    type = models.CharField(
        _('Type'), max_length=3, blank=False, null=False,
        choices=InstituteLicensePlans.LICENSE_PLANS_IN_INSTITUTE_LICENSE)
    billing = models.CharField(
        _('Billing'), max_length=1, blank=False, null=False,
        choices=Billing.BILLING_MODES_IN_INSTITUTE_BILLING)
    amount = models.BigIntegerField(  # In Rs
        _('Amount In Rs'), blank=False, null=False)
    discount_percent = models.DecimalField(
        _('Discount In Percentage'), default=0.0,
        max_digits=5, decimal_places=2)
    storage = models.IntegerField(  # In Gb
        _('Storage in Gb'), blank=False, null=False)
    no_of_admin = models.PositiveIntegerField(
        _('No of admin'), default=1)
    no_of_staff = models.PositiveIntegerField(
        _('No of staff'), default=0)
    no_of_faculty = models.PositiveIntegerField(
        _('No of faculty'), default=0)
    no_of_student = models.PositiveIntegerField(
        _('No of students'), default=UNLIMITED)
    video_call_max_attendees = models.PositiveIntegerField(
        _('Video call max attendees'), blank=False, null=False)
    classroom_limit = models.PositiveIntegerField(
        _('Classroom Limit'), default=UNLIMITED)
    department_limit = models.PositiveIntegerField(
        _('Department Limit'), default=0)
    subject_limit = models.PositiveIntegerField(
        _('Subject Limit'), default=UNLIMITED)
    scheduled_test = models.BooleanField(
        _('Scheduled Test'), default=True)
    LMS_exists = models.BooleanField(
        _('LMS exists'), default=True)
    discussion_forum = models.CharField(
        _('Discussion forum'), max_length=1, blank=False, null=False,
        choices=DiscussionForumBar.DISCUSSION_FORUM_BAR_IN_DISCUSSION_FORUMS)

    def save(self, *args, **kwargs):
        """Overriding save method to allow only superuser
        to create license"""
        if not User.objects.get(email=self.user).is_superuser:
            raise PermissionDenied()

        return super(InstituteLicense, self).save(*args, **kwargs)

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
    discount_rs = models.BigIntegerField(
        _('Discount in Rupees'), blank=False, null=False)
    created_date = models.DateTimeField(
        _('Created Date'), default=timezone.now, editable=False)
    expiry_date = models.DateTimeField(
        _('Expiry Date'), blank=False, null=False)
    coupon_code = models.SlugField(
        _('Coupon Code'), blank=True, null=False, unique=True)
    active = models.BooleanField(_('Active'), default=True)

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


class InstituteSelectedLicense(models.Model):
    """
    Create institute selected license model to store
    selected license plans at that moment
    """
    institute = models.ForeignKey(
        'Institute', related_name='institute_selected_license',
        on_delete=models.CASCADE)
    type = models.CharField(
        _('Type'), max_length=3, blank=False, null=False,
        choices=InstituteLicensePlans.LICENSE_PLANS_IN_INSTITUTE_LICENSE)
    billing = models.CharField(
        _('Billing'), max_length=1, blank=False, null=False,
        choices=Billing.BILLING_MODES_IN_INSTITUTE_BILLING)
    amount = models.DecimalField(  # In Rs
        _('Amount In Rs'), max_digits=10, decimal_places=2,
        blank=False, null=False)
    discount_percent = models.DecimalField(
        _('Discount In Percentage'), default=0.0,
        max_digits=5, decimal_places=2)
    discount_coupon = models.OneToOneField(
        to='InstituteDiscountCoupon', on_delete=models.SET_NULL,
        blank=True, null=True
    )
    net_amount = models.DecimalField(
        _('Net Amount in Rs'), max_digits=10, decimal_places=2,
        blank=True, null=True)
    storage = models.IntegerField(  # In Gb
        _('Storage in GB'), blank=False, null=False)
    no_of_admin = models.PositiveIntegerField(
        _('No of admin'), blank=False, null=False)
    no_of_staff = models.PositiveIntegerField(
        _('No of staff'), blank=False, null=False)
    no_of_faculty = models.PositiveIntegerField(
        _('No of faculty'), blank=False, null=False)
    no_of_student = models.PositiveIntegerField(
        _('No of students'), blank=False, null=False)
    video_call_max_attendees = models.PositiveIntegerField(
        _('Video call max attendees'), blank=False, null=False)
    classroom_limit = models.PositiveIntegerField(
        _('Classroom Limit'), blank=False, null=False)
    department_limit = models.PositiveIntegerField(
        _('Department Limit'), blank=False, null=False)
    subject_limit = models.PositiveIntegerField(
        _('Subject Limit'), blank=False, null=False)
    scheduled_test = models.BooleanField(
        _('Scheduled Test'), blank=False, null=False)
    LMS_exists = models.BooleanField(
        _('LMS exists'), blank=True, null=False)
    discussion_forum = models.CharField(
        _('Discussion forum'), max_length=1, blank=False, null=False,
        choices=DiscussionForumBar.DISCUSSION_FORUM_BAR_IN_DISCUSSION_FORUMS)

    def save(self, *args, **kwargs):
        if self.discount_coupon:
            if not self.discount_coupon.active:
                raise ValueError({'discount_coupon': _('Coupon already used.')})

            if timezone.now() > self.discount_coupon.expiry_date:
                raise ValueError({'discount_coupon': _('Coupon expired.')})

        super(InstituteSelectedLicense, self).save(*args, **kwargs)

    def __str__(self):
        return 'License: ' + str(self.type) + ', billed: ' + str(self.billing)


@receiver(post_save, sender=InstituteSelectedLicense)
def calculate_net_amount(sender, instance, created, *args, **kwargs):
    """Calculates net amount to be paid"""
    if created and not instance.net_amount:
        if instance.discount_coupon:
            instance.net_amount = max(0, instance.amount * (
                    1 - instance.discount_percent / 100) -
                                      instance.discount_coupon.discount_rs)
        else:
            instance.net_amount = max(0, instance.amount * (
                    1 - instance.discount_percent / 100))
        instance.save()

        if instance.discount_coupon:
            instance.discount_coupon.active = False
            instance.discount_coupon.save()


class InstituteLicenseOrderDetails(models.Model):
    """Model to store institute license order"""
    order_receipt = models.CharField(
        _('Order receipt'), max_length=27, blank=True, null=False)
    order_id = models.CharField(
        _('Order Id'), max_length=100, blank=True, null=False)
    amount = models.DecimalField(
        _('Amount in Rupees'), max_digits=10, decimal_places=2,
        blank=True, null=False)
    currency = models.CharField(
        _('Currency'), default='INR', null=False, max_length=4)
    institute = models.ForeignKey(
        'Institute', on_delete=models.SET_NULL,
        related_name='institute_license_order', null=True, blank=False)
    selected_license = models.OneToOneField(
        to='InstituteSelectedLicense', on_delete=models.SET_NULL,
        null=True)
    payment_gateway = models.CharField(
        _('Payment gateway'), max_length=1, null=False, blank=False,
        choices=PaymentGateway.PAYMENT_GATEWAY_IN_PAYMENT_GATEWAYS)
    active = models.BooleanField(
        _('Active'), default=False, blank=True, null=False)
    paid = models.BooleanField(
        _('Paid'), default=False, blank=True, null=False)
    order_created_on = models.DateTimeField(
        _('Order Created On'), default=timezone.now, editable=False)
    payment_date = models.DateTimeField(
        _('Payment Date'), null=True, blank=True)
    start_date = models.DateTimeField(
        _('License Start Date'), blank=True, null=True)
    end_date = models.DateTimeField(
        _('License Expiry Date'), blank=True, null=True)

    def __str__(self):
        return self.order_receipt

    class Meta:
        unique_together = ('institute', 'selected_license')


@receiver(pre_save, sender=InstituteLicenseOrderDetails)
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
    institute_license_order_details = models.ForeignKey(
        InstituteLicenseOrderDetails,
        on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='institute_license_order_details')


class RazorpayWebHookCallback(models.Model):
    """Stores Razorpay webhook callback credentials"""
    order_id = models.CharField(
        _('Razorpay order id'), max_length=100,
        blank=False, null=False)
    razorpay_payment_id = models.CharField(
        _('Razorpay payment id'), max_length=100,
        blank=False, null=False)


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
        'Institute', related_name='permissions', on_delete=models.CASCADE
    )
    inviter = models.ForeignKey(
        'User', related_name='invites', on_delete=models.SET_NULL,
        null=True
    )
    invitee = models.ForeignKey(
        'User', related_name='requests', on_delete=models.CASCADE
    )
    role = models.CharField(
        _('Permission'),
        choices=InstituteRole.ROLE_IN_INSTITUTE_ROLES,
        max_length=1,
        null=False,
        blank=False
    )
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
    name = models.CharField(_('Name'), max_length=25, blank=False)
    order = models.PositiveIntegerField(_('Order'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = unique_key_generator_for_subject_view_name(
                self.view_subject)
        if self.name:
            self.name = self.name.strip()
        if not self.name:
            raise ValueError('Name is required and can not be blank.')
        self.key = self.key.upper()
        super(SubjectViewNames, self).save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        unique_together = ('view_subject', 'key')


@receiver(post_save, sender=SubjectViewNames)
def set_order_automatically(sender, instance, created, *args, **kwargs):
    if created:
        instance.order = instance.pk
        instance.save()
        SubjectViewWeek.objects.create(
            week_view=instance,
            value=1
        )


class SubjectViewWeek(models.Model):
    """Model for storing week details"""
    week_view = models.ForeignKey(
        SubjectViewNames, on_delete=models.CASCADE, related_name='week_view')
    value = models.PositiveIntegerField(
        _('Value'), blank=False, null=False)

    def __str__(self):
        return str(self.value)


class InstituteSubjectCourseContent(models.Model):
    """Model for storing subject content"""
    course_content_subject = models.ForeignKey(
        to='InstituteSubject', related_name='course_content_subject',
        on_delete=models.CASCADE)
    order = models.IntegerField(_('Order'), blank=True, null=True)
    title = models.CharField(
        _('Title'), max_length=30, blank=False, null=False)
    content_type = models.CharField(
        _('Content Type'),
        max_length=1,
        null=False,
        blank=False,
        choices=StudyMaterialContentType.CONTENT_TYPE_IN_CONTENT_TYPES)
    view = models.ForeignKey(
        SubjectViewNames, on_delete=models.CASCADE, related_name='view')
    target_date = models.DateField(
        _('Target Date'), max_length=10, blank=True, null=True)
    uploaded_on = models.DateTimeField(
        _('Uploaded on'), default=timezone.now, editable=False)
    description = models.TextField(_('Description'), default='', blank=True)
    week = models.ForeignKey(
        SubjectViewWeek, on_delete=models.CASCADE, related_name="week",
        blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.title:
            raise ValueError({'error': _('Subject is required.')})
        if not self.content_type:
            raise ValueError({'error': _('Content type is required.')})
        if not self.view:
            raise ValueError({'error': _('View is required.')})
        if self.description:
            self.description = self.description.strip()
        self.title = self.title.strip()
        super(InstituteSubjectCourseContent, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


@receiver(post_save, sender=InstituteSubjectCourseContent)
def add_order_sequence(sender, instance, created, *args, **kwargs):
    if created and not instance.order:
        instance.order = instance.pk
        instance.save()


class SubjectExternalLinkStudyMaterial(models.Model):
    """Model for storing link for institute subject study material"""
    external_link_study_material = models.OneToOneField(
        to='InstituteSubjectCourseContent', related_name='external_link_study_material',
        on_delete=models.CASCADE)
    url = models.CharField(_('Url'), max_length=256, blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.url:
            raise ValueError({'error': _('Url is required.')})
        self.url = self.url.strip()
        super(SubjectExternalLinkStudyMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.external_link_study_material)


class SubjectImageStudyMaterial(models.Model):
    """Model for storing image study material"""
    image_study_material = models.OneToOneField(
        to='InstituteSubjectCourseContent', related_name='image_study_material',
        on_delete=models.CASCADE)
    file = models.FileField(
        _('File'),
        upload_to=subject_img_study_material_upload_file_path,
        null=False,
        blank=False,
        max_length=1024,
        unique=True)
    can_download = models.BooleanField(
        _('Can Download'), blank=True, default=True)

    def save(self, *args, **kwargs):
        if not self.file:
            raise ValueError({'error': _('File is required.')})
        super(SubjectImageStudyMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.image_study_material)


@receiver(post_delete, sender=SubjectImageStudyMaterial)
def auto_delete_image_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        size = Decimal(instance.file.size)
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
            except Exception as e:
                print('Error: ' + e)


class SubjectVideoStudyMaterial(models.Model):
    """Model for storing video study material"""
    video_study_material = models.OneToOneField(
        to='InstituteSubjectCourseContent', related_name='video_study_material',
        on_delete=models.CASCADE)
    file = models.FileField(
        _('File'),
        upload_to=subject_video_study_material_upload_file_path,
        null=False,
        blank=False,
        max_length=1024,
        unique=True)
    size = models.DecimalField(
        _('File size in Gb'), max_digits=12,
        decimal_places=6, null=True, blank=True)
    bit_rate = models.PositiveIntegerField(
        _('Bit Rate'), null=True, blank=True)
    duration = models.DecimalField(
        _('Duration in seconds'), max_digits=10, decimal_places=2, blank=True, null=True)
    stream_file = models.CharField(
        _('HLS encoded stream file'), max_length=1024, blank=True)
    can_download = models.BooleanField(
        _('Can Download'), blank=True, default=True)
    error_transcoding = models.BooleanField(
        _('Error in transcoding'), default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.file:
            raise ValueError({'error': _('File is required.')})
        super(SubjectVideoStudyMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.video_study_material)


@receiver(post_delete, sender=SubjectVideoStudyMaterial)
def auto_delete_video_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
            except Exception as e:
                print('Error: ' + e)


class SubjectPdfStudyMaterial(models.Model):
    """Model for storing pdf study material"""
    pdf_study_material = models.OneToOneField(
        to='InstituteSubjectCourseContent', related_name='pdf_study_material',
        on_delete=models.CASCADE)
    file = models.FileField(
        _('File'),
        upload_to=subject_pdf_study_material_upload_file_path,
        null=False,
        blank=False,
        max_length=1024,
        unique=True)
    duration = models.PositiveIntegerField(
        _('Duration in seconds'), null=True, blank=True)
    total_pages = models.PositiveIntegerField(
        _('Total pages'), null=True, blank=True)
    can_download = models.BooleanField(
        _('Can Download'), blank=True, default=True)

    def save(self, *args, **kwargs):
        if not self.file:
            raise ValueError({'error': _('File is required.')})
        super(SubjectPdfStudyMaterial, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pdf_study_material)


@receiver(post_delete, sender=SubjectPdfStudyMaterial)
def auto_delete_pdf_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
            except Exception as e:
                print('Error: ' + e)


class InstituteStudents(models.Model):
    """Model for storing student in institute"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_student_user')
    institute = models.ForeignKey(
        Institute, on_delete=models.CASCADE, related_name='institute_student_institute')
    roll_no = models.CharField(
        _('Roll no'), max_length=10, blank=True, default='')
    first_name = models.CharField(
        _('First name'), max_length=30, blank=True, default='')
    last_name = models.CharField(
        _('Last name'), max_length=30, blank=True, default='')
    created_on = models.DateTimeField(
        _('Created on'), default=timezone.now, blank=True)
    edited = models.BooleanField(
        _('Edited'), default=False, blank=True)
    active = models.BooleanField(
        _('Edited'), default=False, blank=True)

    def save(self, *args, **kwargs):
        if self.roll_no:
            self.roll_no = self.roll_no.lower().strip()
        if self.first_name:
            self.first_name = self.first_name.lower().strip()
        if self.last_name:
            self.last_name = self.last_name.lower().strip()
        super(InstituteStudents, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    class Meta:
        unique_together = ('user', 'institute')


class InstituteClassStudents(models.Model):
    """Model for storing institute class students"""
    institute_class = models.ForeignKey(
        InstituteClass, on_delete=models.CASCADE, related_name='student_institute_class')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='institute_class_student')
    active = models.BooleanField(_('Active'), default=False, blank=True)
    is_banned = models.BooleanField(_('Is Banned'), default=False, blank=True)

    def __str__(self):
        return str(self.user)
