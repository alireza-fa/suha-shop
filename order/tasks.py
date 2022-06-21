from celery import shared_task
from django.db import transaction
from order.models import Order
from A.local_settings import *
from order.zarinpal import ZP_API_VERIFY
import requests
import json


@shared_task
def verify_payment():
    orders = Order.objects.filter(status=0, authority__isnull=False, is_special=False)
    for order in orders:
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": ZARINPAL_MERCHANT,
            "amount": order.get_total_price() * 10,
            "authority": order.authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                with transaction.atomic():
                    order.ref_id = req.json()['data']['ref_id']
                    order.status = 1
                    order.save()
                    order.save_product()
        else:
            order.need_checkout = True
            order.save()


@shared_task
def verify_special_payment():
    orders = Order.objects.filter(status=0, authority__isnull=False, is_special=True)
    for order in orders:
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": ZARINPAL_MERCHANT,
            "amount": order.special_price * 10,
            "authority": order.authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                with transaction.atomic():
                    order.ref_id = req.json()['data']['ref_id']
                    order.status = 1
                    order.save()
        else:
            order.need_checkout = True
            order.save()
