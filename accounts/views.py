from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from notification.models import Notification
from .forms import VerifyOptCodeForm, UserProfileEditForm, UserChangePasswordForm, ForgetPasswordForm, \
    UserLoginRegisterForm
from django.core.cache import cache
from permissions import NotLoginPermissionMixin, VerifyCodePermissionMixin, SendAgainOtpCodePermissionMixin
from django.contrib.auth import login, logout
from .tasks import send_new_password_task, send_code_task
import random
from django.views.generic.base import TemplateView


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('core:home')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class UserProfileEditView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_edit.html'
    class_form = UserProfileEditForm

    def get(self, request):
        global profile_edit_url
        profile_edit_url = request.GET.get('next', '/accounts/profile/')
        return render(request, self.template_name, {"form": self.class_form(instance=request.user)})

    def post(self, request):
        form = self.class_form(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                user=request.user, title='ویرایش اطلاعات', type=Notification.ALARM,
                message='اطلاعات پروفایل شما با موفقیت تغییر یافت.'
            )
            if profile_edit_url:
                return redirect(profile_edit_url)
            return redirect('core:home')
        messages.warning(request, 'لطفا ارور های زیر را برطرف کنید.')
        return render(request, self.template_name, {"form": form})


class UserChangePassword(LoginRequiredMixin, View):
    template_name = 'accounts/change_password.html'
    class_form = UserChangePasswordForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form()})

    def post(self, request):
        form = self.class_form(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(request, user)
            return JsonResponse(data={"status": 'ok', "url": '/accounts/change_password_success/'})
        string = render_to_string('accounts/ajax/change_password.html', {"form": form})
        return JsonResponse(data={"data": string, "status": 'bad'}, safe=False)


class ChangePasswordSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/change_password_success.html'


class UserForgetPasswordView(LoginRequiredMixin, View):
    template_name = 'accounts/forget_password.html'
    class_form = ForgetPasswordForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form()})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            send_new_password_task.delay(form.cleaned_data['phone_number'])
            return JsonResponse(data={"status": 'ok', "url": '/accounts/forget_password_success/'})
        string = render_to_string('accounts/ajax/forget_password.html', {"form": form})
        return JsonResponse(data={"data": string, "status": 'bad'})


class UserForgetPasswordConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/forget_password_success.html'


class UserFavoriteListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/wish_list.html'


class UserLoginRegisterView(NotLoginPermissionMixin, View):
    template_name = 'accounts/login_register.html'
    class_form = UserLoginRegisterForm

    def get(self, request):
        url = request.GET.get('next', '/')
        request.session['next'] = url
        return render(request, self.template_name, {"form": self.class_form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            form.save(request)
            return JsonResponse(data={"status": 'ok', "url": '/accounts/verify_phone/'})
        string = render_to_string('accounts/ajax/login_register.html', {"form": form})
        return JsonResponse(data={"data": string, "status": 'bad'})


class UserVerifyPhone(VerifyCodePermissionMixin, View):
    template_name = 'accounts/otp_confirm.html'
    class_form = VerifyOptCodeForm

    def get(self, request):
        return render(request, self.template_name, {"form": self.class_form(request)})

    def post(self, request):
        form = self.class_form(data=request.POST, request=request)
        if form.is_valid():
            instance = form.save(request)
            del request.session['login_register']
            login(request, instance)
            url = request.session.get('next', '/')
            return JsonResponse(data={"url": url, "status": 'ok'})
        s = render_to_string('accounts/ajax/otp_confirm.html', {"form": form})
        return JsonResponse(data={"data": s}, safe=False)


class AgainSendOtpCodeView(SendAgainOtpCodePermissionMixin, View):
    def get(self, request):
        phone_number = request.session['login_register']['phone_number']
        rand = str(random.randint(1000, 9999))
        send_code_task.delay(phone_number, rand)
        cache.set(phone_number, rand, timeout=120)
        cache.close()
        return redirect('accounts:verify_phone')
