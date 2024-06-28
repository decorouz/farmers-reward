from django.contrib import admin

from farmers.models import (
    CultivatedCrop,
    CultivatedField,
    CultivatedFieldHistory,
    Farmer,
    FarmersCooperative,
    FarmersMarketTransaction,
    FieldExtensionOfficer,
    Shock,
)

# Register your models here.
admin.site.register(FarmersCooperative)


@admin.register(FieldExtensionOfficer)
class FieldExtensionOfficerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "gender",
        "date_of_birth",
        "age",
        "education",
        "state_of_origin",
        "state_of_residence",
    )
    list_select_related = ("state_of_origin", "state_of_residence")


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "age",
        "education",
        "state_of_origin",
        "state_of_residence",
        "phone_number",
        "cooperative_society",
        "field_extension_officer",
        "category_type",
        "agricultural_activities",
        "farmsize",
        "verification_status",
        "verification_date",
    )


@admin.register(FarmersMarketTransaction)
class FarmersMarketTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "farmer",
        "market",
        "produce",
        "quantity",
        "created_on",
        "points_earned",
    )
    list_select_related = ("farmer", "market", "produce")
    list_filter = ("created_on", "farmer")


@admin.register(CultivatedField)
class CultivatedFieldAdmin(admin.ModelAdmin):
    list_display = (
        "farmer",
        "field_size",
        "town",
        "region",
        "sub_region",
        "country",
        "latitude",
        "logitude",
        "soil_type",
        "soil_test_date",
        "test_results_file",
    )
    list_select_related = ("farmer", "region", "sub_region", "country")
    list_filter = ("sub_region", "country")


@admin.register(CultivatedFieldHistory)
class CultivatedFieldHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "cultivated_field",
        "farming_system",
        "year",
        "primary_crop_type",
    )
    list_select_related = ("cultivated_field",)
    list_filter = ("year",)


@admin.register(CultivatedCrop)
class CultivatedCropAdmin(admin.ModelAdmin):
    list_display = ("field", "crop", "planting_date", "harvest_date", "yield_amount")
    list_select_related = ("field", "crop")
    list_filter = ("crop", "harvest_date", "planting_date")


@admin.register(Shock)
class ShockAdmin(admin.ModelAdmin):
    pass
