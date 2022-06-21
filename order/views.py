from django.db import transaction
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from .zarinpal import send_request, ZP_API_STARTPAY, ZP_API_VERIFY
from .models import Order
from basket.cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from A.local_settings import *
import requests
import json
from .forms import OrderTrackingForm
from permissions import LoginAndAdminRequiredMixin
from django.utils import timezone


class OrderPaymentView(LoginRequiredMixin, View):
    template_error = 'order/payment_error.html'

    def get(self, request):
        cart = Cart(request)
        Order.objects.filter(user=request.user, status=0, authority__isnull=True).delete()
        order = Order.objects.create(user=request.user, status=0)
        if request.session.get('discount'):
            order.discount_code = request.session['discount']['code']
            order.save()
        for item in cart:
            order_item = order.items.create(product=item['product'], quantity=item['quantity'])
            if item['product_color']:
                for product_color in item['product_color'].values():
                    order_item.product_colors.create(product_color=product_color['color'], quantity=int(product_color['quantity']))
        authority, status = send_request(
            order.get_total_price() * 10, description=ZARINPAL_DESCRIPTION, mobile=order.user.phone_number,
            email=order.user.email
        )
        if not status:
            return render(request, self.template_error, {"message": authority})
        order.authority = authority
        order.save()
        return redirect(ZP_API_STARTPAY.format(authority=order.authority))


class OrderVerifyView(LoginRequiredMixin, View):
    template_success = 'order/payment_success.html'
    template_error = 'order/payment_error.html'

    def get(self, request):
        t_authority = request.GET['Authority']
        order = get_object_or_404(Order, authority=t_authority)
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            if order.is_special:
                req_data = {
                    "merchant_id": ZARINPAL_MERCHANT,
                    "amount": order.special_price * 10,
                    "authority": order.authority
                }
            else:
                req_data = {
                    "merchant_id": ZARINPAL_MERCHANT,
                    "amount": order.get_total_price() * 10,
                    "authority": order.authority
                }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                cart = Cart(request)
                if t_status == 100:
                    if not order.is_special:
                        cart.remove()
                    with transaction.atomic():
                        order.ref_id = req.json()['data']['ref_id']
                        order.status = 1
                        order.save()
                        if not order.is_special:
                            order.save_product()
                    return render(request, self.template_success)
                elif t_status == 101:
                    return render(request, self.template_success)
                else:
                    return render(request, self.template_error)
            else:
                return render(request, self.template_error)
        else:
            return render(request, self.template_error)


class OrderTrackingView(LoginRequiredMixin, View):
    template_name = 'order/tracking.html'
    class_form = OrderTrackingForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form(request)})

    def post(self, request):
        form = self.class_form(data=request.POST, request=request)
        if form.is_valid():
            return JsonResponse(data={"status": 'ok', "url": f'/order/detail/{form.cleaned_data.get("code")}/'})
        string = render_to_string('order/ajax/tracking_form.html', {"form": form})
        return JsonResponse(data={"status": 'bad', "data": string})


class OrderDetailView(LoginRequiredMixin, View):
    model = Order
    template_name = 'order/order_status.html'

    def get(self, request, pk):
        if request.user.is_admin:
            order = Order.objects.filter(pk=pk)
        else:
            order = Order.objects.filter(pk=pk, user=request.user, status__gte=1)
        if not order.exists():
            raise Http404()
        return render(request, self.template_name, {"order": order.first()})


class OrderDetailAdminView(LoginAndAdminRequiredMixin, View):
    template_name = 'order/order_detail.html'

    def get(self, request, status=None):
        if status or status == 0:
            orders = Order.objects.filter(status=status)
        else:
            orders = Order.objects.all()
        return render(request, self.template_name, {"orders": orders})


class OrderChangeStatusView(LoginAndAdminRequiredMixin, View):

    def get(self, request, order_id, status):
        if status == 4:
            return redirect('order:details', status)
        order = get_object_or_404(Order, id=order_id)
        num = order.status
        order.status = num + 1
        order.save()
        return redirect('order:details', status)


class SpecialOrderPaymentView(LoginRequiredMixin, View):
    template_error = 'order/payment_error.html'

    def get(self, request, order_id):
        now = timezone.now()
        three_day_ago = now - timezone.timedelta(days=3)
        order = Order.objects.filter(user=request.user, status=0, id=order_id, created__gte=three_day_ago)
        if order.exists():
            order = order.first()
        else:
            raise Http404()
        authority, status = send_request(
            order.special_price * 10, description=ZARINPAL_DESCRIPTION, mobile=order.user.phone_number,
            email=order.user.email
        )
        if not status:
            return render(request, self.template_error, {"message": authority})
        order.authority = authority
        order.save()
        return redirect(ZP_API_STARTPAY.format(authority=authority))
