from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Contact(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(unique=True)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}-{self.email}"
