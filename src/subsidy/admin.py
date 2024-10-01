from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    AgriculturalInput,
    InputCollection,
    Subsidy,
    SubsidyApplication,
    SubsidyCategory,
    SubsidyDisbursement,
    SubsidyInstance,
)


class FarmInputCollectionInline(TabularInline):
    model = AgriculturalInput
    extra = 1


@admin.register(InputCollection)
class CollectionAdmin(ModelAdmin):
    list_display = ("type",)

    inlines = [FarmInputCollectionInline]


@admin.register(Subsidy)
class SubsidyProgramAdmin(ModelAdmin):
    list_display = (
        "title",
        "program_sponsor",
        "rate",
        "level",
        "country",
        "state",
        "current_num_of_beneficiaries",
    )
    list_filter = ("level",)
    list_select_related = ("state", "country")
    autocomplete_fields = ("state",)
    prepopulated_fields = {"slug": ("title", "state", "program_sponsor")}


@admin.register(AgriculturalInput)
class FarmInputAdmin(ModelAdmin):
    list_display = ("company", "name", "unit_price", "unit")
    search_fields = ("name",)
    list_filter = ("company",)
    list_select_related = ("collection",)


@admin.register(SubsidyApplication)
class SubsidyApplicationAdmin(ModelAdmin):
    list_display = ("farmer", "subsidy", "application_date", "approval_status")
    list_filter = ("approval_status", "subsidy", "application_date")
    list_select_related = ("farmer", "subsidy")


@admin.register(SubsidyDisbursement)
class SubsidyDisbursementAdmin(ModelAdmin):
    list_display = (
        "application",
        "disbursement_date",
        "total_value_items",
        "subsidized_amount",
    )
    list_filter = ("disbursement_date",)
    list_select_related = ("application",)


@admin.register(SubsidyCategory)
class SubsidyCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(SubsidyInstance)
class SubsidyInstanceAdmin(ModelAdmin):
    list_display = (
        "id",
        "subsidy",
        "category",
        "quantity",
        "instance_rate",
    )
    list_filter = ("subsidy", "category")
    list_select_related = ("subsidy", "category")
