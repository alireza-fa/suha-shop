from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class IsActiveManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Notification(models.Model):
    ALARM = 'alarm'
    DROPBOX = 'dropbox'
    REPLY = 'reply'
    SHIP = 'ship'
    HEART = 'heart-filled'
    THUNDER = 'thunder'
    OFFER = 'offer'

    NOTIFICATION_TYPE = (
        (ALARM, 'آلارم'),
        (DROPBOX, 'دراپ باکس'),
        (REPLY, 'بازخورد'),
        (SHIP, 'حمل و نقل'),
        (HEART, 'علاقه مندی'),
        (THUNDER, 'رعد و برق'),
        (OFFER, 'آفر')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True, verbose_name=_('user'))
    title = models.CharField(max_length=120, verbose_name=_('title'))
    type = models.CharField(choices=NOTIFICATION_TYPE, max_length=50)
    message = RichTextField(verbose_name=_('message'))
    link = models.CharField(max_length=240, null=True, blank=True, verbose_name=_('link'))
    is_see = models.BooleanField(default=False, verbose_name=_('is see'))
    is_sms = models.BooleanField(default=False, verbose_name=_('is sms'))
    is_send = models.BooleanField(default=False, verbose_name=_('is send'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    time_to_send = models.DateTimeField(verbose_name=_('time to send'), null=True, blank=True)
    expire_time = models.DateTimeField(verbose_name=_('expire time'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f'{self.title[:30]} - {self.get_type_display()}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('notification:notification_detail', args=[self.pk])
