from django import forms
from convert_numbers import persian_to_english
from catalogue.models import Discount
from django.utils.translation import gettext_lazy as _


class AddCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput())
    color = forms.CharField(required=False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(AddCartForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = persian_to_english(self.cleaned_data.get('quantity'))
        quantity = int(quantity)
        if not 1 < quantity < 10:
            return 1
        return quantity

    def get_quantity(self, product):
        quantity = self.cleaned_data['quantity']
        extant = product.count - product.purchase_count
        if quantity > extant:
            quantity = extant
        product_cart = self.request.session['cart'].get(str(product.id))
        if product_cart:
            total_quantity = product_cart['quantity'] + quantity
            if total_quantity > extant:
                ex = extant - product_cart['quantity']
                if ex >= 0:
                    return ex
                return 0
        return quantity

    def get_color(self, product, quantity):
        color = self.cleaned_data.get('color')
        if color:
            try:
                color = int(color)
            except:
                return None, None
            product_color = product.colors.filter(color__id=color)
            if product_color.exists():
                product_color = product_color.first()
                product_cart = self.request.session['cart'].get(str(product.id))
                if product_cart:
                    product_color_cart = product_cart['product_color'].get(str(product_color.id))
                    if product_color_cart:
                        total_quantity = product_color_cart['quantity'] + quantity
                        extant = product_color.count
                        if total_quantity > extant:
                            ex = extant - product_color_cart['quantity']
                            if ex > 0:
                                return product_color, ex
                            return product_color, 0
                        return product_color, quantity
                if product_color.count > quantity:
                    return product_color, quantity
                else:
                    return product_color, product_color.count
        else:
            return None, None
        return None, None


class DiscountCodeForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', "id": 'code', "placeholder": _('Discount code')}),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(DiscountCodeForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        discount = Discount.objects.filter(code=code)
        if discount.exists():
            discount = discount.first()
            if discount.is_private:
                if discount.user != self.request.user:
                    raise forms.ValidationError(_('This code is a privacy code and you do not own it.'))
            if discount.is_limit:
                if not discount.time_use:
                    raise forms.ValidationError(_('Invalid discount code.'))
                discount.time_use -= 1
                discount.save()
            return code
        raise forms.ValidationError(_('Invalid discount code.'))
