from django.contrib import admin

from farmers.models import (
    CultivatedField,
    Farmer,
    FarmersAccountDetail,
    FarmersCooperative,
    FarmersMarketTransaction,
    FieldExtensionOfficer,
)

# Register your models here.
admin.site.register(FarmersCooperative)
admin.site.register(FarmersAccountDetail)
admin.site.register(Farmer)
admin.site.register(FieldExtensionOfficer)
admin.site.register(FarmersMarketTransaction)
admin.site.register(CultivatedField)
