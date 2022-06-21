from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from catalogue.models import Product
from .cart import Cart
from .forms import AddCartForm, DiscountCodeForm


class UserCartView(View):
    template_name = 'basket/cart.html'
    cart = Cart
    class_form = DiscountCodeForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form(request=request)})

    def post(self, request):
        form = self.class_form(request=request, data=request.POST)
        if form.is_valid():
            cart = self.cart(request)
            cart.add_discount_code(form.cleaned_data['code'])
            return JsonResponse(data={"status": 'ok'})
        string = render_to_string('basket/ajax/discount_form.html', {"form": form})
        return JsonResponse(data={"data": string, "status": 'bad'})


class UserCheckoutView(LoginRequiredMixin, View):
    template_name = 'basket/checkout.html'

    def get(self, request):
        return render(request, self.template_name)


class AddProductToCartView(View):
    class_form = AddCartForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart = Cart(request)
        form = AddCartForm(data=request.GET, request=request)
        if form.is_valid():
            quan = form.get_quantity(product)
            color, quantity = form.get_color(product, quan)
            if color:
                cart.add(product, quantity, color)
            else:
                quantity = quan
                cart.add(product, quantity)
            string = render_to_string('catalogue/ajax/alert_detail.html')
            return JsonResponse(data={"status": 'ok', "data": string})
        return JsonResponse(data={"status": 'bad'})


class ChangeQuantity(View):
    cart = Cart
    class_form = AddCartForm

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = self.cart(request)
        form = AddCartForm(data=request.GET, request=request)
        if form.is_valid():
            quantity = form.get_quantity(product)
            cart.change_quantity(product.id, quantity)
            return redirect('basket:cart')
        return redirect('basket:cart')


class RemoveItemView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove_item(product.id)
        return redirect('basket:cart')
