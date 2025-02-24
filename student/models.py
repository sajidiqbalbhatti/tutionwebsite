from django.db import models
from django.conf import settings
from courses.models import Course
from django.core.exceptions import ValidationError


class Student(models.Model):
    # Define category choices
    CATEGORY_CHOICES = [
        ('IG', 'IGs'),
        ('FSC', 'FSC'),
        ('MAT', 'Matric'),
        ('OTH', 'Other'),
    ]

    LEVEL_CHOICES = [
        ('O', 'Ordinary Level (O-Level)'),
        ('A', 'Advanced Level (A-Level)'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Use the custom user model
        on_delete=models.CASCADE,
        
    )



     # Store student's name
    
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='OTH',
        null=False
    )  # Field for IGs, FSC, Matric, etc.
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        null=True,
        blank=True,
        help_text="Select the academic level of the student."
    )
    name=models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    enrolled_courses = models.ManyToManyField('courses.Course', related_name="enrolled_students", blank=True)
    parent_name = models.CharField(max_length=100, null=True, blank=True)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enrolled_courses = models.ManyToManyField('courses.Course', related_name="enrolled_students", blank=True)
    # def enroll_in_course(self, course):
    #     """Enroll student in a course only if they are not already enrolled."""
    #     if self.enrolled_courses.filter(id=course.id).exists():
    #         raise ValidationError(f"You are already enrolled in {course.title}.")
    #     self.enrolled_courses.add(course)

    def __str__(self):
        return self.name

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
