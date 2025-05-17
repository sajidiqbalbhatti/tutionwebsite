from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from Notification.models import Notification
from courses.models import Course
from student.models import Student
from assignments.models import Assignment
from Tutor.models import TutorProfile

User = get_user_model()

# Notify Admins, Tutors, and Students when a Course is Added by any Tutor
tutors_courses_signal = m2m_changed
@receiver(m2m_changed, sender=TutorProfile.courses.through)
def notify_all_on_course_addition(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for course_id in pk_set:
            try:
                course = Course.objects.get(pk=course_id)
                # Notify all Admins
                admins = User.objects.filter(is_superuser=True)
                for admin in admins:
                    tutor_name = course.created_by.tutorprofile.name
                    Notification.objects.create(
                        user=admin,
                        message=f"📚 New course '{course.title}' has been added by tutor {tutor_name}.",
                        link=f"/admin/courses/course/{course.id}/change/"
                    )
                # Notify all Tutors
                tutors = TutorProfile.objects.all()
                for tutor in tutors:
                    tutor_name = course.created_by.tutorprofile.name
                    Notification.objects.create(
                        user=tutor.user,
                        message=f"🎓 New course '{course.title}' has been added by tutor {tutor_name}",
                        link=f"/Tutor/tutor_dashboard/"
                    )
                # Notify all Students
                students = Student.objects.all()
                for student in students:
                    if student.user.is_authenticated:
                        tutor_name = course.created_by.tutorprofile.name
                        Notification.objects.create(
                            user=student.user,
                            message=f"📘 A new course '{course.title}' has been added, by {tutor_name}",
                            link=f"/student/student_dashboard/"
                        )
            except Course.DoesNotExist:
                pass

# Notify Admin when a Course is updated by any Tutor
@receiver(post_save, sender=Course)
def notify_admin_on_course_update(sender, instance, created, **kwargs):
    if not created:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                message=f"🔄 The course '{instance.title}' has been updated by tutor {instance.created_by.username}.",
                link=f"/admin/courses/course/{instance.id}/change/"
            )

# Notify Admin when a Course is deleted by any Tutor
@receiver(pre_delete, sender=Course)
def notify_admin_on_course_delete(sender, instance, **kwargs):
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=f"🗑️ The course '{instance.title}' has been deleted by tutor {instance.created_by.username}.",
            link=f"/admin/courses/course/{instance.id}/change/"
        )


# Assignments signals   

@receiver(post_save, sender=Assignment)
def notify_on_assignment_creation(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        tutor = instance.tutor
        assignment_title = instance.title

        # Notify students enrolled in this course
        enrolled_students = Student.objects.filter(enrolled_courses=course)
        for student in enrolled_students:
            Notification.objects.create(
                user=student.user,
                message=f"📝 A new assignment '{assignment_title}' has been added in your course: '{course.title}'.",
                link=f"/student/assignments/{instance.id}/"
            )

        # Notify Admins
        admin_users = User.objects.filter(role=User.ADMIN)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=f"📣 Tutor '{tutor.user.get_full_name()}' created an assignment '{assignment_title}' in course '{course.title}'.",
                link=f"/admin/assignments/{instance.id}/"
            )