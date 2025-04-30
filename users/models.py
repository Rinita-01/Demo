from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=False, blank=True, null=True)  # Allow blank usernames
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        null=True, blank=True
    )
    address = models.TextField(null=True, blank=True)
    user_type = models.CharField(
        max_length=10, choices=[('customer', 'Customer'), ('admin', 'Admin')],
        default='customer'  # Default to 'customer'
    )
    # otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Login with email instead of username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Removed 'username' since it's optional

    def save(self, *args, **kwargs):
        # Auto-generate a username if it's blank
        if not self.username:
            self.username = f"user_{self.email.split('@')[0]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email  # Using email as the primary identifier
