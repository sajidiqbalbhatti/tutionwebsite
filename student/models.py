from django.db import models 
from django.conf import settings
from courses.models import Course
from Tutor.models import TutorProfile
from PIL import Image

class Student(models.Model):
    """Represents a student profile in the system."""
    
    CATEGORY_CHOICES = [
        ('SCI', 'Science'),
        ('TECH', 'Technology'),
        ('ARTS', 'Arts'),
        ('COMM', 'Commerce'),
        ('OTH', 'Other'),
    ]

    GRADE_CHOICES = [
        ('O-Level', 'Ordinary Level (O-Level)'),
        ('A-level', 'Advanced Level (A-Level)'),
        ('FSC', 'FSC'),
        ('ICS', 'ICS'),
        ('OTH', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='OTH'
    )

    level = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        null=True,
        blank=True,
        help_text="Select the academic level of the student."
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    enrolled_courses = models.ManyToManyField(Course, related_name="enrolled_students")
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            self.resize_image()

    def resize_image(self):
        img = Image.open(self.profile_picture.path)
        if img.width > 1000 or img.height > 1000:
            img.thumbnail((1000, 1000), Image.LANCZOS)  # High-quality resize
            img.save(self.profile_picture.path, quality=95)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enrolled_tutors = models.ManyToManyField(TutorProfile, related_name='students')

    def __str__(self):
        courses = ", ".join(course.title for course in self.enrolled_courses.all()) or "No Courses"
        return f"{self.user.username} ({courses})"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
