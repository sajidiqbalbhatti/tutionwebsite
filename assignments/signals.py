from django.utils.html import escape
from django.db.models.signals import post_save
from django.dispatch import receiver
from Notification.models import Notification
from .models import AssignmentSubmission
from users.models import User  # Replace with your actual user model import

@receiver(post_save, sender=AssignmentSubmission)
def notify_tutor_and_admin_on_submission(sender, instance, created, **kwargs):
    if created:
        assignment = instance.assignment
        student = instance.student
        tutor = assignment.tutor

        # Notify the tutor
        Notification.objects.create(
            user=tutor.user,
            message=(
                f"📥 Student <strong>{escape(student.user.get_full_name())}</strong> "
                f"has submitted the assignment '<strong>{escape(assignment.title)}</strong>' "
                f"for course '<strong>{escape(assignment.course.title)}</strong>'."
            ),
            link=f"/Tutor/assignment-submissions/{assignment.id}/"
        )

        # Notify all admins
        admin_users = User.objects.filter(role=User.ADMIN)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=(
                    f"📢 Student <strong>{escape(student.user.get_full_name())}</strong> "
                    f"has submitted assignment '<strong>{escape(assignment.title)}</strong>' "
                    f"for course '<strong>{escape(assignment.course.title)}</strong>'."
                ),
                link=f"/admin/assignment-submissions/{assignment.id}/"
            )
