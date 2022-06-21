from django import forms
from .models import Contact
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.ModelForm):
    website = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": 'form-control mb-3', "id": 'website', "placeholder": _('Your website name(optional)')}),
        required=False
    )

    class Meta:
        model = Contact
        fields = ('name', 'phone_number', 'website', 'message')

        widgets = {
            "name": forms.TextInput(attrs={"class": 'form-control mb-3', "id": 'name', "placeholder": _('Your name')}),
            "phone_number": forms.TextInput(attrs={"class": 'form-control mb-3', "id": 'phone_number', "placeholder": _('Your phone number')}),
            "message": forms.Textarea(attrs={"class": 'form-control mb-3', "id": 'message', "cols": '30', "rows": '10', "placeholder": _('Write thing...')})
        }

    def clean_name(self):
        if len(self.cleaned_data.get('name')) > 32:
            raise forms.ValidationError(_('Name field must be less than 32 character.'))
        return self.cleaned_data.get('name')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if len(phone) != 11 or not phone.startswith('09'):
            raise forms.ValidationError(_('Invalid phone number'))
        try:
            phone = int(phone)
        except:
            raise forms.ValidationError(_('Invalid phone number.'))
        return self.cleaned_data.get('phone_number')

    def clean_website(self):
        if len(self.cleaned_data.get('website')) > 50:
            raise forms.ValidationError(_('Your website address must be less than 50 character.'))
        return self.cleaned_data.get('website')
