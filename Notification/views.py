from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    ordering = ['-created_at']

    def get_queryset(self):
       return Notification.objects.filter(recipient=self.request.user)


class MarkNotificationAsReadView(LoginRequiredMixin, UpdateView):
    model = Notification
    fields = []  # No form fields needed, just updating is_read

    def get(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, id=self.kwargs['pk'], recipient=self.request.user)
        notification.is_read = True
        notification.save()
        return redirect(reverse_lazy('notifications:list'))
