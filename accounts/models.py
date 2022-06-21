from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True, verbose_name=_('username'))
    fullname = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('fullname'))
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('phone number'))
    email = models.EmailField(max_length=120, unique=True, null=True, blank=True, verbose_name=_('email'))
    address = models.TextField(max_length=420, null=True, blank=True, verbose_name=_('address'))
    post_code = models.PositiveBigIntegerField(null=True, blank=True, verbose_name=_('post code'))
    image = models.ImageField(default='avatar.jpg', verbose_name=_('image'))
    score = models.PositiveIntegerField(default=0, verbose_name=_('score'))
    notification_active = models.BooleanField(default=True, verbose_name=_('notification active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))

    # My Manager
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ('username', 'email')

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
