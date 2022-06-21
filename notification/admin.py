from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_send', 'is_see', 'is_active', 'is_sms', 'time_to_send')
    list_filter = ('is_sms', 'is_send', 'is_see', 'is_active', 'is_sms')
    search_fields = ('title', 'message', 'user__username', 'user__phone_number')
