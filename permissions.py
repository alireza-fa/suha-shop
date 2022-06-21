from django.http import Http404
from django.shortcuts import redirect
from django.core.cache import cache


class NotLoginPermissionMixin:
    url_redirect = 'core:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)


class VerifyCodePermissionMixin:
    url_redirect = 'accounts:login_register'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        info = request.session.get('login_register')
        if not info:
            return redirect(self.url_redirect)
        if not cache.get(key=info['phone_number']):
            return redirect(self.url_redirect)
        return super().dispatch(request, *args, **kwargs)


class SendAgainOtpCodePermissionMixin:
    url_redirect = 'accounts:login_register'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        info = request.session.get('login_register')
        if not info:
            return redirect(self.url_redirect)
        return super().dispatch(request, *args, **kwargs)


class RequiredLoginInPostMixin:
    url_redirect = 'accounts:login_register'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and not request.user.is_authenticated:
            return redirect(self.url_redirect)
        return super().dispatch(request, *args, **kwargs)


class LoginAndAdminRequiredMixin:
    url_redirect = 'accounts:login_register'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()
        if not request.user.is_admin:
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
