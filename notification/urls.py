from django.urls import path
from . import views


app_name = 'notification'
urlpatterns = [
    path('', views.NotificationView.as_view(), name='notifications'),
    path('detail/<int:pk>/', views.NotificationDetailView.as_view(), name='notification_detail'),
    path('remove/', views.NotificationRemoveView.as_view(), name='remove'),
]
