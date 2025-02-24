from django.db import models
from Tutor.models import TutorProfile
from django.contrib.auth import get_user_model
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Get User model
User = get_user_model()

class LearningMode(models.TextChoices):
    ONLINE = "Online", "Online"
    COLLEGE = "College", "College"
    ACADEMY = "Academy", "Academy"
    HOME_TUITION = "Home Tuition", "Home Tuition"

class LearningModeOption(models.Model):
    mode = models.CharField(max_length=20, choices=LearningMode.choices, unique=True)

    def __str__(self):
        return self.get_mode_display()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Category '{self.name}' saved")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Category '{self.name}' deleted")
        super().delete(*args, **kwargs)

class Level(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Level '{self.name}' saved")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Level '{self.name}' deleted")
        super().delete(*args, **kwargs)

class Subject(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='subjects')
    subject_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.level} - {self.subject_name}"

    def save(self, *args, **kwargs):
        logger.info(f"Subject '{self.level} - {self.subject_name}' saved")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Subject '{self.level} - {self.subject_name}' deleted")
        super().delete(*args, **kwargs)

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'tutor'},
        related_name='courses_taught',
        null=True,
        blank=True,
    )
    students = models.ManyToManyField(
        User,
        limit_choices_to={'role': 'student'},
        related_name='courses_enrolled',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
    )
    teacher = models.ForeignKey(TutorProfile, on_delete=models.CASCADE, null=True, blank=True)

    mode = models.ManyToManyField(LearningModeOption)
    course_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration = models.PositiveIntegerField(help_text='Duration in hours')
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    content = models.TextField(help_text='Course content or syllabus', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        logger.info(f"Course '{self.title}' saved")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Course '{self.title}' deleted")
        super().delete(*args, **kwargs)

    def enroll_student(self, student):
        """Enroll a student in the course."""
        if student.role == 'student':
            self.students.add(student)
            self.save()
            logger.info(f"Student '{student.username}' enrolled in course '{self.title}'")

    def get_enrolled_students(self):
        """Return the list of enrolled students."""
        return self.students.all()
