from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Contact


# Register your models here.
@admin.register(Contact)
class AdminContact(ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "message",
        "created_at",
    )
