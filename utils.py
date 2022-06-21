import random
from A import local_settings
from kavenegar import *


class Sms:
    """
        Note:
            for use this method, need to write task.
    """
    API_KEY = local_settings.KAVE_API_KEY
    SENDER = local_settings.KAVE_SENDER
    MESSAGE = None

    def send(self, receiver, message):
        try:
            api = KavenegarAPI(self.API_KEY)
            params = {
                'sender': self.SENDER,
                'receptor': receiver,
                'message': message,
            }
            response = api.sms_send(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)

    def send_otp_code(self, code, phone_number):
        self.send(receiver=phone_number, message=f'کد: {code}')
        return code

    def send_new_password(self, phone_number):
        password = str(random.randint(10000, 99999))
        self.send(receiver=phone_number, message=f'کلمه عبور جدید شما: {password}')
        return password

    def send_code(self, phone_number, code, password=None):
        self.send(receiver=phone_number, message=f'کد شما: {code}')
        return code

    def send_status_order(self, phone_number, message):
        self.send(receiver=phone_number, message=message)
        return True

    def send_sms(self, phone_number, message):
        self.send(receiver=phone_number, message=message)
        return True


sms = Sms()
