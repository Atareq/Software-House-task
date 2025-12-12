from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    SALES = "sales", "Sales"


class CustomUser(AbstractUser):

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.SALES,
    )
