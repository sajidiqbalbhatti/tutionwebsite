from django.db import models

# Create your models here.
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from student.models import Student  # Assuming Student model is in 'students' app
from Tutor.models import TutorProfile  # Assuming TutorProfile model is in 'tutors' app

User = get_user_model()


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, related_name='created_assignments')  # Changed from User to TutorProfile
    due_date = models.DateTimeField()
    max_marks = models.PositiveIntegerField(default=100)  # Ensuring only positive marks
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')  # Changed from User to Student
    submitted_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)
    graded = models.BooleanField(default=False)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)  # Ensuring only positive marks
    feedback = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.submitted_at:
           self.submitted_at = now()  # Assign the current timestamp if not set

        if self.assignment.due_date and self.submitted_at and self.submitted_at > self.assignment.due_date:
            self.is_late = True

        super().save(*args, **kwargs)