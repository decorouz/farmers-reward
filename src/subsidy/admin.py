from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

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
class SubsidyRateInline(admin.TabularInline):
    model = SubsidyRate
    extra = 1


class SubsidyInstanceInline(admin.TabularInline):
    model = SubsidyInstance
    extra = 1


class SubsidizedItemInline(GenericTabularInline):
    model = SubsidizedItem
    extra = 1


# Define admin classes with relevant configurations
@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fertilizer_type",
        "name",
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
class SeedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "seed_variety",
        "gmo",
        # "current_price",
        # "unit",
    )
    search_fields = ("name", "seed_variety")
    list_filter = ("name", "gmo")
    inlines = [SubsidizedItemInline]


@admin.register(Mechanization)
class MechanizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        # "current_price",
        # "unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    inlines = [SubsidizedItemInline]


@admin.register(Agrochemical)
class AgrochemicalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "agrochemical_name",
        # "current_price",
        # "unit",
    )
    search_fields = ("name", "agrochemical_name")
    list_filter = ("agrochemical_name",)
    inlines = [SubsidizedItemInline]


@admin.register(SubsidyProgram)
class SubsidyProgramAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "sponsor_name",
        "number_of_beneficiaries",
        "legislation",
        "country",
        "region",
        "start_date",
        "end_date",
        "is_active",
    )
    list_select_related = ("country", "region")
    search_fields = ("sponsor_name", "region__name")
    list_filter = ("sponsor_name", "is_active", "start_date", "end_date")
    raw_id_fields = ("country", "region")
    inlines = [SubsidyRateInline, SubsidyInstanceInline]


@admin.register(SubsidizedItem)
class SubsidizedItemAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "content_type",
        "object_id",
        "subsidized_item",
        # "current_price",
    )
    search_fields = ("type",)
    ordering = ["type"]
    list_filter = ("type", "date")
    inlines = [SubsidyRateInline]

    def current_price(self, obj):
        return obj.subsidized_item.current_price


@admin.register(SubsidyRate)
class SubsidyRateAdmin(admin.ModelAdmin):
    list_display = ("subsidy_program", "subsidized_item", "rate")
    search_fields = ("subsidy_program__title", "subsidized_item__subsidized_item")
    list_selected_related = ("subsidy_program", "subsidized_item")
    list_filter = ("rate",)


@admin.register(SubsidyInstance)
class SubsidyInstanceAdmin(admin.ModelAdmin):
    list_display = (
        "farmer",
        "item",
        "subsidy_program",
        "quantity",
        "item_unit",
        # "original_price",
        "discounted_price",
        "total_discounted_price",
        "redemption_date",
    )
    search_fields = (
        "farmer__name",
        "item__subsidized_item",
        "subsidy_program__title",
    )
    list_filter = ("redemption_date",)
    raw_id_fields = ("farmer", "item", "subsidy_program")

    def total_discounted_price(self, obj):
        return obj.quantity * obj.discounted_price


@admin.register(InputPriceHistory)
class InputPriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "content_type",
        "object_id",
        "item",
        "price",
        "created_on",
    )
    search_fields = ("item",)
    ordering = ["created_on"]
    list_filter = ("created_on",)
