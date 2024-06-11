from django.contrib import admin

from subsidy.models import FarmerSubsidy, SubsidyProgram

# Register your models here.
admin.site.register(FarmerSubsidy)
admin.site.register(SubsidyProgram)
