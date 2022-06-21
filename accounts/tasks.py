from celery import shared_task
from accounts.models import User
from utils import sms


@shared_task
def send_otp_code_tasks(code, phone_number):
    code = sms.send_otp_code(code=code, phone_number=phone_number)
    return code


@shared_task
def send_new_password_task(phone_number):
    user = User.objects.filter(phone_number=phone_number)
    if user.exists():
        password = sms.send_new_password(phone_number=phone_number)
        use = user.first()
        use.set_password(password)
        use.save()
        return True


@shared_task
def send_code_task(phone_number, code, password=None):
    result = sms.send_code(phone_number, code)
    return result
