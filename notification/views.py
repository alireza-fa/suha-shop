from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Notification


class NotificationView(LoginRequiredMixin, View):
    template_name = 'notification/notifications.html'

    def get(self, request):
        return render(request, self.template_name)


class NotificationDetailView(LoginRequiredMixin, View):
    template_name = 'notification/notification_detail.html'
    model = Notification

    def get(self, request, pk):
        notif = get_object_or_404(self.model, pk=pk)
        if notif.user == request.user or not notif.user:
            notif.is_see = True
            notif.save()
            return render(request, self.template_name, {"notif": notif})
        return redirect('notification:notifications')


class NotificationRemoveView(LoginRequiredMixin, View):
    def get(self, request):
        request.user.notifications.all().delete()
        return redirect('notification:notifications')
