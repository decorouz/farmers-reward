from django.db import models

from core.models import TimeStampedPhoneModel


# Create your models here.
class Contact(TimeStampedPhoneModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.email}"
