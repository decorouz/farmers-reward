import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    """An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields."""

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(verbose_name="email address", unique=True)
