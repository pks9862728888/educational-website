from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import EmailValidator, MinLengthValidator, \
    ProhibitNullCharactersValidator
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework.authtoken.models import Token


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


class Subject(models.Model):
    """Creates subject model where only teacher can create subject"""
    user = models.ForeignKey(
        'User', related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(
        _('Subject name'), max_length=30, blank=False, null=False,
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

        super(Subject, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('user', 'name')
