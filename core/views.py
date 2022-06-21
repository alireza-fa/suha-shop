from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page, cache_control
from django.views.generic.base import TemplateView
from django.views import View
from .forms import ContactForm
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .models import  SiteSetting


class HomeView(TemplateView):
    template_name = 'core/home.html'


class SettingsView(View):
    template_name = 'core/settings.html'

    def get(self, request):
        return render(request, self.template_name)


class ContactUsView(View):
    template_name = 'core/contact.html'
    class_form = ContactForm

    def get(self, request):
        form = self.class_form()
        if request.user.is_authenticated:
            form = self.class_form(initial={"phone_number": request.user.phone_number})
        return render(request, self.template_name, {"form": form, "setting": SiteSetting.objects.last()})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            form.save()
            string = render_to_string('core/ajax/contact_success.html', {"form": self.class_form()})
            return JsonResponse(data={"status": 'ok', "data": string})
        string = render_to_string('core/ajax/contact.html', {"form": form})
        return JsonResponse(data={"data": string, "status": 'bad'})


@method_decorator([cache_page(86400), cache_control(public=True, private=True)], name='dispatch')
class AboutUsView(TemplateView):
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = {"setting": SiteSetting.objects.last()}
        return context


@method_decorator([cache_page(2678400), cache_control(public=True, private=True)], name='dispatch')
class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'
