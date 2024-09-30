from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class TimeStampModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampModel):
    phone = PhoneNumberField(max_length=14, blank=True, null=True, unique=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True)
