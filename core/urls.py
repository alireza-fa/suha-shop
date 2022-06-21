from django.urls import path
from core import views
from django.views.generic.base import TemplateView


app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('offline/', TemplateView.as_view(template_name='offline.html'), name='offline')
]
