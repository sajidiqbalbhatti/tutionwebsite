from django.db import models
from django.conf import settings

from PIL import Image

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

    def __str__(self):
        
        return self.name

class TutorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tutorprofile'
    )
    name = models.CharField(max_length=255)
    bio = models.TextField()
    education = models.CharField(max_length=255)
    certifications = models.CharField(max_length=255)
    subjects = models.ManyToManyField(Subject, related_name='tutors') 
    courses = models.ManyToManyField("courses.Course", related_name='tutors')  # ✅ Fix: String path

    experience_years = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    languages_spoken = models.CharField(max_length=255)

    profile_picture = models.ImageField(upload_to='tutor_profiles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            self.resize_image()

    def resize_image(self):
        img = Image.open(self.profile_picture.path)
        if img.width > 1000 or img.height > 1000:
            img.thumbnail((1000, 1000), Image.LANCZOS)  # High-quality resize
            img.save(self.profile_picture.path, quality=95)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)  # Avg rating from students
    available_from = models.TimeField()
    available_until = models.TimeField()

    def __str__(self):
        return self.user.username

from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
