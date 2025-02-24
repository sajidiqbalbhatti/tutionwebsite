from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    TUTOR = 'tutor'
    STUDENT = 'student'
    PARENT = 'parent'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TUTOR, 'Tutor'),
        (STUDENT, 'Student'),
        (PARENT, 'Parent'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ADMIN,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Use a unique name for reverse accessor
        blank=True,
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Use a unique name for reverse accessor
        blank=True,
    )

    def __str__(self):
        return self.username

    
class UserManager(models.Manager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a regular user with the given username and password.
        """
        if not username:
            raise ValueError('The username field must be set')
        
        # Set a default role for regular users if not provided
        extra_fields.setdefault('role', User.ADMIN)
        
        # Create the user
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with the given username and password.
        """
        # Ensure the role is set to User.ADMIN
        extra_fields.setdefault('role', User.ADMIN)

        # Add superuser-specific fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Validate the superuser flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

