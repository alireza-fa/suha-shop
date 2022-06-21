from django import forms
import convert_numbers
from order.models import Order
from django.utils.translation import gettext_lazy as _


class OrderTrackingForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', "id": 'code', "placeholder": _('Tracking code')})
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(OrderTrackingForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            code = convert_numbers.persian_to_english(code)
            if self.request.user.is_admin:
                order = Order.objects.filter(id=code)
            else:
                order = Order.objects.filter(id=code, user=self.request.user, status__gte=1)
            if not order.exists():
                raise forms.ValidationError(_('Invalid tracking code.'))
        return code
