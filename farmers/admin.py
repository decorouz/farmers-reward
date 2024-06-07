from django.contrib import admin

from farmers.models import (
    CultivatedField,
    Farmer,
    FarmersAccountDetail,
    FarmersCooperative,
    FarmerSubsidy,
    FieldExtensionOfficer,
    SaleTransaction,
    SubsidyProgram,
)

# Register your models here.
admin.site.register(FarmersCooperative)
admin.site.register(FarmersAccountDetail)
admin.site.register(Farmer)
admin.site.register(FieldExtensionOfficer)
admin.site.register(SubsidyProgram)
admin.site.register(FarmerSubsidy)
admin.site.register(SaleTransaction)
admin.site.register(CultivatedField)
