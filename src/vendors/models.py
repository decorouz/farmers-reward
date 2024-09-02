from django.db import models

from core.models import BaseModel

# Create your models here.


class AgroVendor(BaseModel):
    name = models.CharField(max_length=100)
    addressof_business = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    lga = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    email = models.EmailField()
    verification_status = models.BooleanField(default=False)
    # When is vendor considered verified?

    def __str__(self) -> str:
        return f"{self.name}"
