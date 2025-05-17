from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Student
from courses.models import Course
from Notification.models import Notification

User = get_user_model()

@receiver(m2m_changed, sender=Student.enrolled_courses.through)
def student_enrolled_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for course_id in pk_set:
            try:
                course = Course.objects.get(pk=course_id)

                # Notify admin(s)
                admins = User.objects.filter(is_superuser=True)
                for admin in admins:
                    student_name = f"{instance.user.first_name} {instance.user.last_name}"
                    tutor_name = course.created_by.tutorprofile.name

                    Notification.objects.create(
                        user=admin,
                        message=f"📥 Student {student_name} enrolled in '{course.title}'. Instructor: {tutor_name}"
                        
   
                    )

                # Notify specific tutor who created the course
                if course.created_by:
                    student_name = f"{instance.user.first_name} {instance.user.last_name}"

                    Notification.objects.create(
                        user=course.created_by,
                        message=f"👨‍🎓 Student {student_name} enrolled in your course: {course.title}."

                    )

            except Course.DoesNotExist:
                pass
