from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Agrochemical,
    Fertilizer,
    MechanizationOperation,
    Seed,
    SubsidizedItem,
    SubsidyInstance,
    SubsidyProgram,
)


@admin.register(Fertilizer)
class FertilizerAdmin(ModelAdmin):
    list_display = (
        "manufacturer",
        "fertilizer_type",
        "fertilizer_blend",
        "unit",
        "price",
    )
    list_filter = ("fertilizer_type",)


@admin.register(Seed)
class SeedAdmin(ModelAdmin):
    list_display = ("seed_company", "crop", "seed_variety", "unit", "price", "gmo")
    list_filter = ("crop", "gmo")


@admin.register(MechanizationOperation)
class MechanizationOperationAdmin(ModelAdmin):
    list_display = ("operation_type", "unit", "price")

    list_filter = ("operation_type",)


@admin.register(Agrochemical)
class AgrochemicalAdmin(ModelAdmin):
    list_display = ("manufacturer", "agrochemical_type", "unit", "price")

    list_filter = ("agrochemical_type",)


@admin.register(SubsidyProgram)
class SubsidyProgramAdmin(ModelAdmin):
    list_display = (
        "title",
        "program_sponsor",
        "rate",
        "level",
        "country",
        "state",
        "current_num_of_beneficiaries",
        "is_active",
    )
    list_filter = (
        "level",
        "is_active",
    )
    list_select_related = ("state", "country")
    autocomplete_fields = ("state",)


@admin.register(SubsidizedItem)
class SubsidizedItemAdmin(ModelAdmin):
    list_display = (
        "type",
        "seed",
        "fertilizer",
        "mechanization",
        "chemical",
        "item_price",
        "item_unit",
    )
    list_filter = ("type",)
    list_select_related = ("seed", "fertilizer", "mechanization", "chemical")


@admin.register(SubsidyInstance)
class SubsidyInstanceAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "item",
        "subsidy_program",
        "quantity",
        "redemption_date",
        "item_unit",
        "redemption_location",
    )
    list_filter = ("subsidy_program", "redemption_date")
    list_select_related = ("farmer", "item", "subsidy_program")
