from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class TimeStampedPhoneModel(models.Model):
    """An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields."""

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    phone = PhoneNumberField(
        region="NG",
        max_length=14,
        blank=True,
        null=True,
        unique=True,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True)
