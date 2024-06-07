from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(verbose_name="email address", unique=True)


class TimeStampedModel(models.Model):
    """An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
