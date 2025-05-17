# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('notifications/read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_read'),
]
