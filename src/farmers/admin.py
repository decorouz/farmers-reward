from django.contrib import admin
from unfold.admin import ModelAdmin

from farmers.models import (
    Badge,
    CultivatedField,
    CultivatedFieldHistory,
    Farmer,
    FarmersCooperative,
    FarmersInputTransaction,
    FarmersMarketTransaction,
    FieldExtensionOfficer,
    Harvest,
    SoilProperty,
    UserBadge,
)


# Register your models here.
@admin.register(FarmersCooperative)
class FarmersCooperativeAdmin(ModelAdmin):
    list_display = (
        "name",
        "chairman",
        "phone_number",
        "registration_number",
        "location",
        "blacklisted",
        "verification_status",
    )


@admin.register(FieldExtensionOfficer)
class FieldExtensionOfficerAdmin(ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "gender",
        "date_of_birth",
        "age",
        "education",
        "state_of_origin",
        "state_of_residence",
        "means_of_identification",
        "identification_number",
    )
    autocomplete_fields = ("state_of_origin", "state_of_residence")
    list_select_related = ("state_of_origin", "state_of_residence")
    prepopulated_fields = {"slug": ("first_name", "last_name", "phone_number")}


@admin.register(Farmer)
class FarmerAdmin(ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "age",
        "education",
        "state_of_origin",
        "lga",
        "state_of_residence",
        "phone_number",
        "cooperative_society",
        "field_extension_officer",
        "category_type",
        "agricultural_activities",
        "farmsize",
        # "verification_status",
        "confirmed_farmer_status",
        "total_points",
        "verification_date",
    )
    list_select_related = (
        "state_of_origin",
        "state_of_residence",
        "cooperative_society",
        "lga",
        "field_extension_officer",
    )
    autocomplete_fields = ("state_of_origin", "state_of_residence", "lga")
    prepopulated_fields = {
        "slug": (
            "first_name",
            "last_name",
            "phone_number",
        )
    }


@admin.register(FarmersMarketTransaction)
class FarmersMarketTransactionAdmin(ModelAdmin):
    list_display = (
        "id",
        "farmer",
        "market",
        "produce",
        "quantity",
        "transaction_date",
        "points_earned",
    )
    list_select_related = ("farmer", "market", "produce")
    list_filter = ("market__id", "farmer")


@admin.register(FarmersInputTransaction)
class FarmersInputTransactionAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "vendor",
        "amount",
        "receipt_identifier",
        "redemption_date",
        "points_earned",
    )
    list_select_related = ("farmer", "vendor")


@admin.register(CultivatedField)
class CultivatedFieldAdmin(ModelAdmin):
    list_display = (
        "field_size",
        "soil_test",
        "town",
        "region",
        "sub_region",
        "country",
        "latitude",
        "logitude",
    )
    list_select_related = ("region", "sub_region", "country")
    list_filter = ("sub_region", "country")


@admin.register(CultivatedFieldHistory)
class CultivatedFieldHistoryAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "farming_system",
        "cultivated_field",
        "farming_system",
        "primary_crop_type",
        "secondary_crop_type",
        "pri_crop_planting_date",
        "sec_crop_planting_date",
        "fertilizer_use",
        "fertilizer_qty",
        "manure_compost_use",
        "average_ridge_weed_biomass",
        "striga",
        "row_spacing",
    )
    list_select_related = ("cultivated_field", "farmer")
    list_filter = ("primary_crop_type",)


@admin.register(Harvest)
class HarvestAdmin(ModelAdmin):
    list_display = (
        "pri_crop",
        "sec_crop",
        "field",
        "pri_crop_harvest_date",
        "sec_crop_harvest_date",
        "pri_yield_amount",
        "sec_yield_amount",
    )

    list_select_related = ("field", "sec_crop", "pri_crop")


@admin.register(SoilProperty)
class SoilPropertyAdmin(ModelAdmin):
    list_display = (
        "cultivated_field",
        "texture",
        "pH",
        "organic_matter",
        "nitrogen_content",
        "phosphorus_content",
        "potassium_content",
        "soil_test_date",
        "soil_lab",
        "soil_test_date",
    )
    list_select_related = ("cultivated_field",)


@admin.register(Badge)
class BadgeAdmin(ModelAdmin):
    list_display = ("name", "image_thumbnail", "points_required")
    list_filter = ("points_required",)
    list_filter = ("name",)


@admin.register(UserBadge)
class UserBadgeAdmin(ModelAdmin):
    list_display = ("farmer", "badge", "earned_on")
    list_select_related = ("farmer", "badge")
    list_filter = ("earned_on", "badge", "farmer")
    list_select_related = ("farmer", "badge")
