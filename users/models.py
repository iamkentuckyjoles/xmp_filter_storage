from django.db import models  # Django ORM for defining model fields
from django.contrib.auth.models import AbstractUser  # Base class for custom user model


# -------------------------------------------------------------------
# Model: CustomUser
# Purpose: Extend Django's default user model with role-based access
# -------------------------------------------------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [  # Role options for access control
        ('admin', 'Admin'),
        ('senior', 'Senior Editor'),
        ('junior', 'Junior Editor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='junior')  # Default role is junior

    def __str__(self):
        return f"{self.username} ({self.role})"  # Display username with role