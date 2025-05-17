# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .models import LoginLog
from Notification.models import Notification

User = get_user_model()

def get_admin_user():
    return User.objects.filter(is_superuser=True).first()

# New User Signup Notification
@receiver(post_save, sender=User)
def notify_admin_on_user_creation(sender, instance, created, **kwargs):
    if created:
        admin_user = get_admin_user()
        if admin_user:
            Notification.objects.create(
                user=admin_user,
                message=f"🆕 New user signed up: {instance.username} ({instance.role})",
                link=f"/admin/users/user/{instance.id}/change/"
            )

# User Login Notification and Logging
@receiver(user_logged_in)
def notify_admin_on_user_login(sender, request, user, **kwargs):
    LoginLog.objects.create(user=user)
    admin_user = get_admin_user()
    if admin_user:
        Notification.objects.create(
            user=admin_user,
            message=f"✅ User logged in: {user.username} at {now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
