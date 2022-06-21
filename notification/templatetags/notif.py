from django import template
from notification.models import Notification
from django.db.models import Q


register = template.Library()


@register.filter(name='get_notif')
def get_notif_filter(user):
    return Notification.objects.filter(Q(user=user) | Q(user=None))
