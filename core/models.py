from django.db import models
from django.utils.translation import gettext_lazy as _
from catalogue.models import Product
from ckeditor.fields import RichTextField


class Contact(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    phone_number = models.CharField(max_length=11, verbose_name=_('phone number'))
    website = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('website'))
    message = models.TextField(verbose_name=_('message'))
    read = models.BooleanField(default=False, verbose_name=_('read or unread'))
    active = models.BooleanField(default=False, verbose_name=_('active or deactive'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ('-created', )

    def __str__(self):
        return f'{self.name} - {self.phone_number}'


class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sliders', verbose_name=_('product'))
    title = models.CharField(max_length=64, verbose_name=_('title'))
    description = models.CharField(max_length=120, verbose_name=_('description'))
    image = models.ImageField(verbose_name=_('image'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        ordering = ('-created', )
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    about_us = RichTextField(verbose_name=_('about us'))
    contact_us = RichTextField(verbose_name=_('contact us'))

    def __str__(self):
        return f'تنظیمات وب سایت'

    class Meta:
        verbose_name = _('Site setting')
        verbose_name_plural = _('Site settings')
