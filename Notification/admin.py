from django.contrib import admin

# Register your models here.
# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)
