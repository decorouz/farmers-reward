from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from unfold.admin import ModelAdmin

from farmers.models import (
    AgroVendor,
    Farmer,
    FarmersInputTransaction,
    FarmersMarketTransaction,
    FieldExtensionOfficer,
)


@admin.register(AgroVendor)
class AgroVendorAdmin(ModelAdmin):
    list_display = (
        "name",
        "state",
        "lga",
        "phone_number",
        "verification_status",
    )
    list_filter = ("verification_status", "state")


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
        "state",
        "means_of_identification",
        "identification_number",
    )
    autocomplete_fields = ("state_of_origin", "state")
    list_select_related = ("state_of_origin", "state")
    prepopulated_fields = {"slug": ("first_name", "last_name", "phone_number")}


@admin.register(Farmer)
class FarmerAdmin(ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "age",
        "education",
        "state_of_origin",
        "lga",
        "state",
        "phone_number",
        "field_extension_officer",
        "category_type",
        "agricultural_activities",
        "farmsize",
        "has_market_transaction",
        "has_input_transaction",
        "is_verified",
        "earned_points",
    )
    list_select_related = (
        "state_of_origin",
        "state",
        "lga",
        "field_extension_officer",
    )

    list_filter = (
        "is_verified",
        "gender",
    )
    autocomplete_fields = ("state_of_origin", "state", "lga")
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
    list_filter = ("market__name", "farmer")


@admin.register(FarmersInputTransaction)
class FarmersInputTransactionAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "vendor",
        "amount",
        "receipt_verification_date",
        "points_earned",
    )
    list_select_related = ("farmer", "vendor")
