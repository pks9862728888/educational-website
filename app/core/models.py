import os
import uuid
import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import EmailValidator, MinLengthValidator, \
    ProhibitNullCharactersValidator, validate_image_file_extension
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from django_countries.fields import CountryField

from rest_framework.authtoken.models import Token


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


def user_profile_picture_upload_file_path(instance, filename):
    """Generates file path for uploading images in user profile"""
    extension = filename.split('.')[-1]
    file_name = f'{uuid.uuid4()}.{extension}'
    date = datetime.date.today()
    path = 'pictures/uploads/user/profile'
    ini_path = f'{path}/{date.year}/{date.month}/{date.day}/'
    full_path = os.path.join(ini_path, file_name)

    return full_path


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
        _('First Name'), max_length=255, blank=True,
        validators=(ProhibitNullCharactersValidator, ))
    last_name = models.CharField(
        _('Last Name'), max_length=255, blank=True,
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


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        # Creating teacher profile
        if instance.is_teacher:
            TeacherProfile.objects.create(user=instance)
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
