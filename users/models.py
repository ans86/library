from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import AppConfig

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('author', 'Author'),
        ('common_user', 'Common User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='common_user')
    can_upload_books = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'