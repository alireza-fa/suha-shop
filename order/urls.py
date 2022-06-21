from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'order'
urlpatterns = [
    path('payment/', views.OrderPaymentView.as_view(), name='payment'),
    path('verify/', views.OrderVerifyView.as_view(), name='verify'),
    path('tracking/', views.OrderTrackingView.as_view(), name='tracking'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('details/', views.OrderDetailAdminView.as_view(), name='details'),
    path('details/<int:status>/', views.OrderDetailAdminView.as_view(), name='details'),
    path('details/change_status/<int:order_id>/<int:status>/', views.OrderChangeStatusView.as_view(), name='change_status'),
    path('special/payment/<int:order_id>/', views.SpecialOrderPaymentView.as_view(), name='special_payment'),
]
