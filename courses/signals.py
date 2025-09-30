# courses/signals.py
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Course

@receiver([post_delete, post_save], sender=Course)
def clear_course_cache(sender, **kwargs):
    print("🗑️ Cache cleared automatically (signal)")
    cache.delete("all_courses")
