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
    
    # Contact & Identification
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(default="default@example.com")

    id_card_number = models.CharField(max_length=20, unique=True)
    id_card_picture = models.ImageField(upload_to='id_cards/')

    # Education & Skills
    education = models.CharField(max_length=255)
    certifications = models.CharField(max_length=255, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='tutors') 
    courses = models.ManyToManyField("courses.Course", related_name='tutors')

    # Work Experience
    experience_years = models.IntegerField()
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    languages_spoken = models.CharField(max_length=255)

    # Profile Picture & Rating
    profile_picture = models.ImageField(upload_to='tutor_profiles/')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)  

    # Availability
    available_from = models.TimeField()
    available_until = models.TimeField()

    # Location
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    # Other
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            self.resize_image(self.profile_picture)
        if self.id_card_picture:
            self.resize_image(self.id_card_picture)

    def resize_image(self, image_field):
        img = Image.open(image_field.path)
        if img.width > 1000 or img.height > 1000:
            img.thumbnail((1000, 1000), Image.LANCZOS)
            img.save(image_field.path, quality=95)

    def __str__(self):
        return self.user.username

    
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
    
