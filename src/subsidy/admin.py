from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Agrochemical,
    Fertilizer,
    InputPriceHistory,
    Mechanization,
    Seed,
    SubsidizedItem,
    SubsidyInstance,
    SubsidyProgram,
    SubsidyRate,
)


# Define inlines for related models
class SubsidyRateInline(TabularInline):
    model = SubsidyRate
    extra = 1


class SubsidyInstanceInline(TabularInline):
    model = SubsidyInstance
    extra = 1


class SubsidizedItemInline(GenericTabularInline):
    model = SubsidizedItem
    extra = 1


# Define admin classes with relevant configurations
@admin.register(Fertilizer)
class FertilizerAdmin(ModelAdmin):
    list_display = (
        "brand",
        "fertilizer_type",
        "fertilizer_blend",
        # "current_price",
        # "unit",
    )
    search_fields = ("fertilizer_type", "name")
    list_filter = (
        "id",
        "fertilizer_type",
    )
    inlines = [SubsidizedItemInline]


@admin.register(Seed)
class SeedAdmin(ModelAdmin):
    list_display = (
        "brand",
        "name",
        "seed_variety",
        "gmo",
        # "current_price",
        # "unit",
    )
    search_fields = ("name", "brand")
    list_filter = ("name", "gmo")
    inlines = [SubsidizedItemInline]


@admin.register(Mechanization)
class MechanizationAdmin(ModelAdmin):
    list_display = (
        "operation",
        # "current_price",
        # "unit",
    )
    search_fields = ("operation",)
    list_filter = ("operation",)
    inlines = [SubsidizedItemInline]


@admin.register(Agrochemical)
class AgrochemicalAdmin(ModelAdmin):
    list_display = (
        "brand",
        "type",
        # "current_price",
        # "unit",
    )
    list_filter = ("type",)
    inlines = [SubsidizedItemInline]


@admin.register(SubsidyProgram)
class SubsidyProgramAdmin(ModelAdmin):
    list_display = (
        "title",
        "sponsor_name",
        "level",
        "target_num_of_beneficiaries",
        "country",
        "state",
        "budget_in_naira",
        "start_date",
        "end_date",
        "is_active",
    )
    list_select_related = ("country", "state")
    list_filter = ("is_active", "level")
    raw_id_fields = ("country", "state")
    inlines = [SubsidyRateInline, SubsidyInstanceInline]


@admin.register(SubsidizedItem)
class SubsidizedItemAdmin(ModelAdmin):
    list_display = (
        "type",
        "content_type",
        "object_id",
        "subsidized_item",
        "item_price",
        "unit",
    )
    list_filter = ("type",)
    inlines = [SubsidyRateInline]

    # def current_price(self, obj):
    #     return obj.subsidized_item.item_price


@admin.register(SubsidyRate)
class SubsidyRateAdmin(ModelAdmin):
    list_display = (
        "subsidy_program",
        "subsidized_item",
        "rate",
    )
    # search_fields = ("subsidy_program__title", "subsidized_item__subsidized_item")
    list_selected_related = ("subsidy_program", "subsidized_item")
    list_filter = ("rate",)


@admin.register(SubsidyInstance)
class SubsidyInstanceAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "item",
        "subsidy_program",
        "quantity",
        "item_unit",
        # "discounted_value",
        "redemption_date",
    )

    list_filter = ("redemption_date",)
    raw_id_fields = ("farmer", "item", "subsidy_program")


@admin.register(InputPriceHistory)
class InputPriceHistoryAdmin(ModelAdmin):
    list_display = ("content_type", "object_id", "item", "price", "effective_date")
    search_fields = ("item",)
    list_filter = ("effective_date",)
