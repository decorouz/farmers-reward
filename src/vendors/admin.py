from django.contrib import admin
from unfold.admin import ModelAdmin

from vendors.models import AgroVendor


# Register your models here.
@admin.register(AgroVendor)
class AgroVendorAdmin(ModelAdmin):
    list_display = (
        "name",
        "addressof_business",
        "state",
        "lga",
        "contact_person",
        "contact_phone",
        "email",
        "verification_status",
    )
