import datetime

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from base.model_choices import DEVICE_TYPE
from base.models import UUIDModel, TimeStampedUUIDModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        if extra_fields.get('is_active') is None:
            extra_fields['is_active'] = True
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, UUIDModel, PermissionsMixin):
    first_name = models.CharField(_('First Name'), max_length=120, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=120, blank=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            './+/-/_ only.'),
                                validators=[validators.RegexValidator(r'^[\w.+-]+$',
                                                                      _('Value may contain only letters,'
                                                                        'numbers and ./+/-/_ characters.')), ],
                                error_messages={'unique': _("A user with that username already exists."),
                                                })

    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text='Designates whether the user can log into this admin site.')

    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # For notification on mobile phone
    device_type = models.CharField(max_length=1, choices=DEVICE_TYPE, null=True, blank=True)
    device_id = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name.strip()

    def clean(self):
        self.username = self.username.lower()


class UserActivationKey(TimeStampedUUIDModel):
    """
    A simple profile which stores an activation key for use during
    user account registration.
    """
    user = models.OneToOneField(User, verbose_name='user')
    activation_key = models.CharField('activation key', max_length=40)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return "{} -> {}".format(self.user, self.activation_key)

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        Key expiration is determined by a two-step process:
        1. If the user has already activated, ``self.activated`` will
           be ``True``. Re-activating is not permitted, and so this
           method returns ``True`` in this case.
        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        """
        expiration_date = datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        return (self.activated or
                (self.modified + expiration_date <= timezone.now()))
