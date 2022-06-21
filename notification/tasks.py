from celery import shared_task
from utils import sms
from notification.models import Notification
from django.utils import timezone


@shared_task
def send_status_order_task(phone_number, message):
    sms.send_status_order(phone_number=phone_number, message=message)


@shared_task
def send_sms_task(phone_number, message):
    result = sms.send_sms(phone_number=phone_number, message=message)
    return result


@shared_task
def period_send_sms():
    notifications = Notification.objects.filter(is_active=True, is_sms=True, is_send=False)
    for notif in notifications:
        sms.send_sms(phone_number=notif.user.phone_number, message=notif.message)
    return True


@shared_task
def remove_previous_notif(days=None):
    now = timezone.now()
    if days:
        delta = now - timezone.timedelta(days=days)
    else:
        delta = now - timezone.timedelta(days=10)
    Notification.objects.filter(created__lte=delta).delete()
    return True
