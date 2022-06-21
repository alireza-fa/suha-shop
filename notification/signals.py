from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from accounts.models import User
from django.utils import timezone
from catalogue.models import ProductComment, Product
from order.models import Order
from notification.tasks import send_status_order_task, send_sms_task
from A.local_settings import URL_ROOT


@receiver(post_save, sender=User)
def register_notif(sender, **kwargs):
    if kwargs['created']:
        notif = Notification.objects.create(
            user=kwargs['instance'], title='به ترنگ شاپ خوش آمدید', type=Notification.ALARM,
            message='به فروشگاه اینترنتی ترنگ شاپ خوش آمدید. ما تمام تلاشمان را میکنیم تا بهترین خدمات را برای شما دوستان عزیز فراهم کنیم.',
            is_sms=True, time_to_send=timezone.now()
        )
        send_sms_task.delay(notif.user.phone_number, notif.message + f'\n{URL_ROOT}')
        notif.is_send = True
        notif.save()


@receiver(post_save, sender=ProductComment)
def comment_create(sender, **kwargs):
    if kwargs['created']:
        Notification.objects.create(
            user=kwargs['instance'].user, title='نقد و نظر شما ثبت شد.', type=Notification.ALARM,
            message=f'نظر شما برای محصول {kwargs["instance"].product} ثبت شد. پس از بازبینی نمایش داده خواهد شد.',
            link=kwargs['instance'].product.get_absolute_url()
        )


@receiver(post_save, sender=ProductComment)
def comment_status(sender, **kwargs):
    if not kwargs['created']:
        if kwargs['instance'].is_read and not kwargs['instance'].is_active:
            Notification.objects.create(
                user=kwargs['instance'].user, title='نقد و نظر شما نمایش داده نمیشود😭', type=Notification.ALARM,
                message=f'نقد و نظر شما برای محصول {kwargs["instance"].product}پس از بازبینی رد شد.',
                link=kwargs['instance'].product.get_absolute_url()
            )
        elif kwargs['instance'].is_active:
            Notification.objects.create(
                user=kwargs['instance'].user, title='نقد و نظر شما در حالت نمایش در‌آمد.', type=Notification.ALARM,
                message=f'نقد و نظر شما برای محصول {kwargs["instance"].product} پس از بازبینی به حالت نمایش برای عموم در آمد. با تشکر بخاطر ثبت نظر خود نسبت به این محصول.',
                link=kwargs['instance'].product.get_absolute_url()
            )


@receiver(post_save, sender=Order)
def order_notif(sender, **kwargs):
    if kwargs['instance'].status == 1:
        notif = Notification.objects.create(
            user=kwargs['instance'].user, title='سفارش شما ثبت شد', type=Notification.ALARM,
            message=f' سفارش شما با کد پیگیری {kwargs["instance"].id} ثبت شده است. مراحل بعدی را به شما اطلاع رسانی خواهیم کرد. همچنین شما میتوانید داخل وب سایت قسمت پیگیری با وارد کردن کد پیگیری وضعیت سفارشتان را مشاهده کنید. اگر هر گونه سوالی پیش آمده است با ما در میان بگذارید. ',
            link=kwargs['instance'].get_absolute_url(), is_sms=True
        )
        send_status_order_task.delay(
            notif.user.phone_number, notif.message + f'\n {URL_ROOT + notif.link}'
        )
        notif.is_send = True
        notif.save()

    elif kwargs['instance'].status == 2:
        notif = Notification.objects.create(
            user=kwargs['instance'].user, title='سفارش شما در حال بسته بندی است.', type=Notification.SHIP,
            message=f'سفارش شما با کد پیگیری {kwargs["instance"].id} در حال بسته بندی و آماده سازی برای ارسال است. ',
            link=kwargs['instance'].get_absolute_url(), is_sms=True
        )
        send_status_order_task.delay(
            notif.user.phone_number, notif.message + f'\n {URL_ROOT + notif.link}'
        )
        notif.is_send = True
        notif.save()

    elif kwargs['instance'].status == 3:
        notif = Notification.objects.create(
            user=kwargs['instance'].user, title='سفارش شما در مرحله حمل و نقل قرار دارد.', type=Notification.SHIP,
            message=f' سفارش شما با کد پیگیری {kwargs["instance"].id} به پستچی تحویل داده شده و بزودی به دست شما میرسد. ',
            link=kwargs['instance'].get_absolute_url(), is_sms=True
        )
        send_status_order_task.delay(
            notif.user.phone_number, notif.message + f'\n {URL_ROOT + notif.link}'
        )
        notif.is_send = True
        notif.save()

    elif kwargs['instance'].status == 4:
        notif = Notification.objects.create(
            user=kwargs['instance'].user, title=f' مراحل ارسال سفارش {kwargs["instance"].id} به اتمام رسید ', type=Notification.HEART,
            message=f'خیلی از شما ممنونیم که از ما خرید کرده اید. لطفا اگر پیشنهاد و انتقادی از ما دارید در میان بگذارید.',
            link=kwargs['instance'].get_absolute_url(), is_sms=True
        )
        send_status_order_task.delay(
            notif.user.phone_number, notif.message + f'\n {URL_ROOT + notif.link}'
        )
        notif.is_send = True
        notif.save()


@receiver(post_save, sender=Order)
def special_order_notif(sender, **kwargs):
    if kwargs['created']:
        if kwargs['instance'].is_special:
            notif = Notification.objects.create(
                user=kwargs['instance'].user, title=f'تبریک😍 سفارش ویژه شما آماده است.', type=Notification.HEART,
                message='دوست عزیز. سفارش ویژه شما آماده برای تحویل است.' + 'لطفا سفارش خود را تا سه روز آینده نهایی کنید. در غیر اینصورت این سفارش دیگر در دسترس نخواهد بود.' + '\n' + 'لینک پرداخت سفارش:',
                link=URL_ROOT + f"/order/special/payment/{kwargs['instance'].id}/"
            )
            send_sms_task.delay(
                notif.user.phone_number,
                'سفارش ویژه شما آماده برای تحویل است' + '\n' + 'جهت نهایی کردن سفارشِ بر روی لینک زیر کلیک کنید:' + '\n' +
                f'{URL_ROOT + notif.get_absolute_url()}'
                )


@receiver(post_save, sender=Product)
def get_limit_count(sender, **kwargs):
    if not kwargs['created']:
        if kwargs['instance'].count <= kwargs['instance'].purchase_count:
            user_admin_phone_numbers = User.objects.filter(is_admin=False).values_list('phone_number', flat=True)
            send_sms_task.delay(
                list(user_admin_phone_numbers),
                'محصول' + kwargs['instance'].title + 'به اتمام رسیده است' + 'لینک:' + f'{URL_ROOT}/{kwargs["instance"].get_absolute_url()}'
            )
