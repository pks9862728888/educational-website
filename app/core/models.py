import os
import datetime
import random
import string
import uuid

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
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify

from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token

from .tasks import create_welcome_message_after_user_creation


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


def random_string_generator(size=10,
                            chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator_for_institute(instance, new_slug=None):
    """Generates unique slug field for institute"""
    if new_slug is not None:
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
                              validators=(EmailValidator, ))
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


class TeacherProfile(models.Model, Languages):
    """Creates user profile model"""
    user = models.OneToOneField(
        'User',
        related_name='teacher_profile',
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        _('First Name'), max_length=70, blank=True,
        validators=(ProhibitNullCharactersValidator, ))
    last_name = models.CharField(
        _('Last Name'), max_length=70, blank=True,
        validators=(ProhibitNullCharactersValidator, ))
    gender = models.CharField(
        _('Gender'),
        max_length=1,
        blank=True,
        choices=Gender.GENDER_IN_GENDER_CHOICES,)
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
        self.first_name = self.first_name.upper().strip()
        self.last_name = self.last_name.upper().strip()

        super(TeacherProfile, self).save(*args, **kwargs)

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
            TeacherProfile.objects.create(user=instance)

        # Creates welcome message using task queue
        if instance.username != os.environ.get('SYSTEM_USER_USERNAME'):
            create_welcome_message_after_user_creation.delay(instance.pk)
    else:
        # Saving teacher profile and creating if not existing
        if instance.is_teacher:
            try:
                instance.teacher_profile.save()
            except ObjectDoesNotExist:
                TeacherProfile.objects.create(user=instance)


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
        self.name = self.name.lower().strip()

        if len(self.name) == 0:
            raise ValueError({'name': _('Institute name can not be blank')})

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


class InstituteAdmin(models.Model):
    """Creates Institute admin permissions model"""
    institute = models.ForeignKey(
        'Institute', related_name='admins', on_delete=models.CASCADE
    )
    inviter = models.ForeignKey(
        'User', related_name='invited_admins', on_delete=models.SET_NULL,
        null=True
    )
    invitee = models.ForeignKey(
        'User', related_name='admin_permission', on_delete=models.CASCADE
    )
    active = models.BooleanField(_('Active'), default=False)
    request_date = models.DateTimeField(
        _('Request Date'), default=timezone.now, editable=False)
    request_accepted_on = models.DateTimeField(
        _('Request Accept Date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        """Overriding save method to check permissions"""
        # Owner of institute can invite himself
        # Only admin can appoint admin
        admin_exists = InstituteAdmin.objects.filter(
            inviter=self.inviter,
            active=True
        ).exists()

        if (not admin_exists) and self.inviter != self.institute.user and self.inviter == self.invitee:
            raise PermissionDenied()

        # Inviter can not pre activate joining of other invitees
        # Only invitee can activate his joining
        entry_exists = InstituteAdmin.objects.filter(
            invitee=self.invitee,
            inviter=self.inviter,
            institute=self.institute
        ).exists()

        if self.active and self.invitee != self.institute.user and not entry_exists:
            raise PermissionDenied()

        # Only teacher user can be appointed as staff
        if not self.invitee.is_teacher:
            raise PermissionDenied()

        super(InstituteAdmin, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('institute', 'invitee')

    def __str__(self):
        return str(self.invitee)


@receiver(post_save, sender=Institute)
def institute_is_created(sender, instance, created, **kwargs):
    if created:
        InstituteProfile.objects.create(institute=instance)
        InstituteAdmin.objects.create(
            institute=instance,
            inviter=instance.user,
            invitee=instance.user,
            active=True
        )
    else:
        try:
            instance.institute_profile.save()
        except ObjectDoesNotExist:
            InstituteProfile.objects.create(institute=instance)


class InstituteStaff(models.Model):
    """Creates Institute staff permissions model"""
    institute = models.ForeignKey(
        'Institute', related_name='staffs', on_delete=models.CASCADE
    )
    inviter = models.ForeignKey(
        'User', related_name='invited_staffs', on_delete=models.SET_NULL,
        null=True
    )
    invitee = models.ForeignKey(
        'User', related_name='staff_permission', on_delete=models.CASCADE
    )
    active = models.BooleanField(_('Active'), default=False)
    request_date = models.DateTimeField(
        _('Request Date'), default=timezone.now, editable=False)
    request_accepted_on = models.DateTimeField(
        _('Request Accept Date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        """Overriding save method to check permissions"""
        # Can not invite self as staff
        if self.inviter == self.invitee:
            raise PermissionDenied()

        # Only active admin can appoint staff
        # Only invitee can activate his joining
        is_active_admin = InstituteAdmin.objects.filter(
            invitee=self.inviter,
            institute=self.institute,
            active=True
        ).exists()

        if not is_active_admin:
            raise PermissionDenied()

        # Inviter can not pre activate joining but invitee can accept
        entry_exists = InstituteStaff.objects.filter(
            invitee=self.invitee,
            institute=self.institute
        ).exists()
        if self.active and (not entry_exists):
            raise PermissionDenied()

        # Only teacher user can be appointed as staff
        if not self.invitee.is_teacher:
            raise PermissionDenied()

        super(InstituteStaff, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('institute', 'invitee')

    def __str__(self):
        return str(self.invitee)


class InstituteFaculty(models.Model):
    """Creates Institute faculty permissions model"""
    institute = models.ForeignKey(
        'Institute', related_name='faculties', on_delete=models.CASCADE
    )
    inviter = models.ForeignKey(
        'User', related_name='invited_faculties', on_delete=models.SET_NULL,
        null=True
    )
    invitee = models.ForeignKey(
        'User', related_name='faculty_permission', on_delete=models.CASCADE
    )
    active = models.BooleanField(_('Active'), default=False)
    request_date = models.DateTimeField(
        _('Request Date'), default=timezone.now, editable=False)
    request_accepted_on = models.DateTimeField(
        _('Request Accept Date'), null=True, blank=True)

    def save(self, *args, **kwargs):
        """Overriding save method to check permissions"""
        # Can not invite self as faculty
        if self.inviter == self.invitee:
            raise PermissionDenied()

        # Only active admin or active staff can appoint faculty
        # Only invitee can activate joining
        is_active_admin = InstituteAdmin.objects.filter(
            invitee=self.inviter,
            institute=self.institute,
            active=True
        ).exists()
        is_active_staff = InstituteStaff.objects.filter(
            invitee=self.inviter,
            institute=self.institute,
            active=True
        ).exists()

        if not is_active_admin and not is_active_staff:
            raise PermissionDenied()

        # Inviter can not pre activate joining but invitee can accept
        entry_exists = InstituteFaculty.objects.filter(
            invitee=self.invitee,
            institute=self.institute
        ).exists()
        if self.active and (not entry_exists):
            raise PermissionDenied()

        # Only teacher user can be appointed as staff
        if not self.invitee.is_teacher:
            raise PermissionDenied()

        super(InstituteFaculty, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('institute', 'invitee')

    def __str__(self):
        return str(self.invitee)


class Classroom(models.Model):
    """Creates classroom model where only teacher can create classroom"""
    user = models.ForeignKey(
        'User', related_name='classroom', on_delete=models.CASCADE)
    name = models.CharField(
        _('Classroom name'), max_length=30, blank=False, null=False,
        validators=(MinLengthValidator(4), ProhibitNullCharactersValidator))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overriding save method"""
        self.name = self.name.lower().strip()

        if len(self.name) == 0:
            raise ValueError({'name': _('Classroom name can not be blank')})

        # Only teachers can create classroom
        if not User.objects.get(email=self.user).is_teacher:
            raise PermissionDenied()

        super(Classroom, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'name')


class Subject(models.Model):
    """Creates subject model where only teacher can create subject"""
    user = models.ForeignKey(
        'User',
        related_name='user_subject',
        on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        'Classroom',
        related_name='classroom_subject',
        on_delete=models.CASCADE)
    name = models.CharField(
        _('Subject name'),
        max_length=30,
        blank=False,
        null=False,
        validators=(MinLengthValidator(4), ProhibitNullCharactersValidator))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overriding save method"""
        self.name = self.name.lower().strip()

        if len(self.name) == 0:
            raise ValueError({'name': _('Subject name can not be blank')})

        # Only teachers can create subject
        if not User.objects.get(email=self.user).is_teacher:
            raise PermissionDenied()

        # Teacher can create subject in his classroom only
        if Classroom.objects.get(name=self.classroom).user != self.user:
            raise PermissionDenied()

        super(Subject, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'classroom', 'name')
