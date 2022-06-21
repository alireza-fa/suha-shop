import convert_numbers
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from .validators import check_phone_number
from accounts.models import User
from django.core.cache import cache
from .tasks import send_code_task
import random
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text=_('you can change password using <a href="../password/">this link</a>'))

    class Meta:
        model = User
        fields = (
            'username', 'phone_number', 'fullname', 'email', 'address', 'post_code',
            'image', 'score', 'notification_active', 'last_login'
        )


class UserProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'fullname', 'email', 'address', 'post_code', 'image')

        widgets = {
            "username": forms.TextInput(attrs={"class": 'form-control', 'maxlength': 32, "id": 'username'}),
            "fullname": forms.TextInput(attrs={"class": 'form-control', "maxlength": 32, "id": 'fullname'}),
            "email": forms.EmailInput(attrs={"class": 'form-control', "maxlength": 120, "id": 'email'}),
            "address": forms.TextInput(attrs={"class": 'form-control', "maxlength": 240, "id": 'address'}),
            "image": forms.FileInput(attrs={"class": 'form-control-file', "id": 'image'}),
            "post_code": forms.NumberInput(attrs={"class": 'form-control', "id": 'post_code'}),
        }

    def clean_username(self):
        cd = self.cleaned_data
        if not cd.get('username') == self.instance.username:
            user = User.objects.filter(username=self.cleaned_data.get('username')).exists()
            if user:
                raise forms.ValidationError(_('This phone number already exists.'))
        return cd.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email == self.instance.email:
            user = User.objects.filter(email=email).exists()
            if user:
                raise forms.ValidationError(_('This email already exists.'))
        return email

    def clean_image(self):
        if self.cleaned_data.get('image').size > 50000:
            raise forms.ValidationError(_('Profile picture must be less than 50kb'))
        return self.cleaned_data.get('image')

    def clean_post_code(self):
        post_code = self.cleaned_data.get('post_code')
        if post_code:
            post_code = convert_numbers.persian_to_english(self.cleaned_data.get('post_code'))
            if len(post_code) != 10:
                raise forms.ValidationError(_('Post number is equal to 10.'))
        return post_code


class UserChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'form-control', "id": 'password'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'form-control', "id": 'new_password'}),
        validators=[
                validators.MinLengthValidator(8, _('Password cannot be less than 8 characters.')),
                validators.MaxLengthValidator(32, _('Password cannot be greater than 32 characters.'))
        ],
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'form-control', "id": 'confirm_password'}),
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        check_pass = self.user.check_password(self.cleaned_data.get('password'))
        if not check_pass:
            raise forms.ValidationError(_('Invalid password.'))
        return self.cleaned_data.get('password')

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd.get('new_password') != cd.get('confirm_password'):
            raise forms.ValidationError(_('New password and confirmation password don\'t match'))
        return cd.get('new_password')


class ForgetPasswordForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', "id": 'phone_number', "maxlength": 11}),
        validators=[check_phone_number],
    )


class UserLoginRegisterForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": 'form-control', "id": 'phone_number', "placeholder": _('Your phone number'), "maxlength": 11}
        ),
        validators=[check_phone_number],
    )

    def save(self, request):
        phone_number = convert_numbers.persian_to_english(self.cleaned_data.get('phone_number'))
        user = User.objects.filter(phone_number=phone_number)
        if user.exists():
            request.session['login_register'] = {"exist": True, "phone_number": phone_number}
        else:
            request.session['login_register'] = {"exist": False, "phone_number": phone_number}
        num = str(random.randint(1000, 9999))
        cache.set(key=phone_number, value=num, timeout=120)
        cache.close()
        send_code_task.delay(phone_number, num)
        return True


class VerifyOptCodeForm(forms.Form):
    code1 = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'single-otp-input form-control', "placeholder": '-', "maxlength": '1', "id": 'code1'}),
        required=True
    )
    code2 = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'single-otp-input form-control', "placeholder": '-', "maxlength": '1', "id": 'code2'}),
        required=True
    )
    code3 = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'single-otp-input form-control', "placeholder": '-', "maxlength": '1', "id": 'code3'}),
        required=True
    )
    code4 = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'single-otp-input form-control', "placeholder": '-', "maxlength": '1', "id": 'code4'}),
        required=True
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(VerifyOptCodeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        clean_code = cd.get('code1', 'n') + cd.get('code2', 'n') + cd.get('code3', 'n') + cd.get('code4', 'n')
        if 'n' in clean_code:
            raise forms.ValidationError(_('Invalid code.'))
        clean_code = convert_numbers.persian_to_english(clean_code)
        phone = self.request.session['login_register']['phone_number']
        code = cache.get(phone)
        cache.close()
        if code != clean_code:
            raise forms.ValidationError(_('Invalid code.'))
        return super().clean()

    def save(self, request):
        if request.session.get('login_register')['exist']:
            user = User.objects.get(phone_number=request.session.get('login_register')['phone_number'])
        elif not request.session.get('login_register')['exist']:
            password = str(random.randint(100000, 999999))
            user = User.objects.create_user(request.session.get('login_register')['phone_number'], password)
        else:
            return None
        return user
