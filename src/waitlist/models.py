from django.db import models

from core.models import BaseModel


# Create your models here.
class Contact(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.email}"
