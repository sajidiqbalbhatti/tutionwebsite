from django.urls import path
from Notification.views import NotificationListView,MarkNotificationAsReadView

app_name='Notifications'
urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('int:notification_id/read/',MarkNotificationAsReadView.as_view(), name='mark_as_read'),
]
