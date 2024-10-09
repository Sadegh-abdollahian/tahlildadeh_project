from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=11, unique=True, verbose_name="شماره موبایل"
    )
    username = models.CharField(max_length=45, verbose_name="نام کاربری")
    has_supscription = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number
