from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    DESIGNATION_CHOICES = [
        ('Manager', 'Manager'),
        ('HR', 'HR'),
        ('Staff', 'Staff'),
    ]

    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(
        max_length=50,
        choices=DESIGNATION_CHOICES,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.username