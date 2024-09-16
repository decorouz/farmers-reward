from django.db import models

from core.models import BaseModel


# Create your models here.
class Contact(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.name}-{self.email}"
