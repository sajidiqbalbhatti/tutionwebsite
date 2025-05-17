from django.shortcuts import get_object_or_404, redirect
from Notification.models import Notification
from users.models import User  # make sure correct path

def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()

    # Define redirects just like get_success_url
    role_redirects = {
        User.ADMIN: 'users:admin_dashboard',
        User.TUTOR: 'Tutor:tutor_dashboard',
        User.STUDENT: 'student:student_dashboard',
        User.PARENT: 'users:parent_dashboard',
    }

    return redirect(role_redirects.get(request.user.role, 'home_page'))  # fallback to home_page
