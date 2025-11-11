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
    

# -------------------------------------------------------------------
# Model: ForgotPasswordRequest
# Purpose: Store password reset requests from users     
# -------------------------------------------------------------------
class ForgotPasswordRequest(models.Model):
    ROLE_CHOICES = [
        ('senior', 'Senior'),
        ('junior', 'Junior'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Handled', 'Handled'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.status}"