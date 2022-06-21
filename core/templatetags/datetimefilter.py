from django import template
from django.utils import timezone
from khayyam import JalaliDatetime


register = template.Library()


@register.filter(name='khayyam')
def khayyam_filter(value):
    return JalaliDatetime(value).strftime('%C')


@register.filter(name='time_active')
def time_active(value):
    if not value:
        return False
    now = timezone.now()
    if value > now:
        return True
    return False
