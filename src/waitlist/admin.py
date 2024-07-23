from django.contrib import admin

from .models import WaitlistEntry


# Register your models here.
@admin.register(WaitlistEntry)
class AdminWaitlisEntry(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
