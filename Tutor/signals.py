from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.cache import cache
from Notification.models import Notification
from courses.models import Course
from student.models import Student
from assignments.models import Assignment
from Tutor.models import TutorProfile

User = get_user_model()


# -----------------------------
# 🔔 COURSE RELATED NOTIFICATIONS
# -----------------------------

@receiver(m2m_changed, sender=TutorProfile.courses.through)
def notify_all_on_course_addition(sender, instance, action, pk_set, **kwargs):
    """Notify Admins, Tutors, and Students when a Tutor adds a Course."""
    if action == "post_add":
        for course_id in pk_set:
            try:
                course = Course.objects.get(pk=course_id)
                tutor_name = course.created_by.tutorprofile.name

                # Notify all Admins
                admins = User.objects.filter(is_superuser=True)
                for admin in admins:
                    Notification.objects.create(
                        user=admin,
                        message=f"📚 New course '{course.title}' has been added by tutor {tutor_name}.",
                        link=f"/admin/courses/course/{course.id}/change/"
                    )

                # Notify all Tutors
                for tutor in TutorProfile.objects.all():
                    Notification.objects.create(
                        user=tutor.user,
                        message=f"🎓 New course '{course.title}' has been added by tutor {tutor_name}.",
                        link="/Tutor/tutor_dashboard/"
                    )

                # Notify all Students
                for student in Student.objects.all():
                    if student.user.is_authenticated:
                        Notification.objects.create(
                            user=student.user,
                            message=f"📘 A new course '{course.title}' has been added by {tutor_name}.",
                            link="/student/student_dashboard/"
                        )

            except Course.DoesNotExist:
                pass


@receiver(post_save, sender=Course)
def notify_admin_on_course_update(sender, instance, created, **kwargs):
    """Notify Admin when a Course is updated."""
    if not created:
        for admin in User.objects.filter(is_superuser=True):
            Notification.objects.create(
                user=admin,
                message=f"🔄 The course '{instance.title}' has been updated by tutor {instance.created_by.username}.",
                link=f"/admin/courses/course/{instance.id}/change/"
            )


@receiver(pre_delete, sender=Course)
def notify_admin_on_course_delete(sender, instance, **kwargs):
    """Notify Admin when a Course is deleted."""
    for admin in User.objects.filter(is_superuser=True):
        Notification.objects.create(
            user=admin,
            message=f"🗑️ The course '{instance.title}' has been deleted by tutor {instance.created_by.username}.",
            link=f"/admin/courses/course/{instance.id}/change/"
        )


# -----------------------------
# 📝 ASSIGNMENT RELATED NOTIFICATIONS
# -----------------------------

@receiver(post_save, sender=Assignment)
def notify_on_assignment_creation(sender, instance, created, **kwargs):
    """Notify Students + Admin when a new Assignment is created."""
    if created:
        course = instance.course
        tutor = instance.tutor
        assignment_title = instance.title

        # Notify students enrolled in this course
        for student in Student.objects.filter(enrolled_courses=course):
            Notification.objects.create(
                user=student.user,
                message=f"📝 A new assignment '{assignment_title}' has been added in your course: '{course.title}'.",
                link=f"/student/assignments/{instance.id}/"
            )

        # Notify Admins
        for admin in User.objects.filter(role=User.ADMIN):
            Notification.objects.create(
                user=admin,
                message=f"📣 Tutor '{tutor.user.get_full_name()}' created an assignment '{assignment_title}' in course '{course.title}'.",
                link=f"/admin/assignments/{instance.id}/"
            )


# -----------------------------
# ⚡ CACHE CLEAR SIGNALS
# -----------------------------

@receiver([post_save, pre_delete], sender=TutorProfile)
def clear_tutor_cache(sender, **kwargs):
    cache.delete("all_tutors")
    print("🗑️ Cache cleared for all_tutors")
