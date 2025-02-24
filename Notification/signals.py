from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification

@receiver(post_save, sender=User)
def create_notification_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # New user created, so we send a welcome notification
        Notification.objects.create(
            user=instance,
            message="Welcome to the platform! You have successfully registered."
        )
