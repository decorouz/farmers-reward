from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin

from core.models import User

# Register your models here.
# admin.site.unregister(User)


# @admin.register(User)
# class UserAdmin(BaseUserAdmin, ModelAdmin):
#     pass
