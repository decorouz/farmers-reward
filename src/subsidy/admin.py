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
        # "unit",
        # "price",
    )
    list_filter = ("fertilizer_type",)


@admin.register(Seed)
class SeedAdmin(ModelAdmin):
    list_display = (
        "seed_company",
        "crop",
        "seed_variety",
        # "unit",
        # "price",
        "gmo",
    )
    list_filter = ("crop", "gmo")


@admin.register(MechanizationOperation)
class MechanizationOperationAdmin(ModelAdmin):
    list_display = (
        "operation_type",
        # "unit",
        # "price",
    )

    list_filter = ("operation_type",)


@admin.register(Agrochemical)
class AgrochemicalAdmin(ModelAdmin):
    list_display = (
        "manufacturer",
        "agrochemical_type",
        "name",
        # "unit",
        # "price",
    )

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
    prepopulated_fields = {"slug": ("title", "state", "program_sponsor")}


from .models import SubsidizedItem, SubsidyInstance, SubsidyInstanceItem


class SubsidizedItemAdmin(ModelAdmin):
    list_display = ("item_name", "item_type", "item_price", "unit")
    list_filter = ("item_type",)
    search_fields = ("item_name", "item_type")

    fieldsets = (
        (None, {"fields": ("item_type", "item_name", "item_price", "unit")}),
        (
            "Related Items",
            {
                "fields": (
                    "fertilizer",
                    "seed",
                    "agrochemical",
                    "mechanization_operation",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("item_type",)
        return ()


class SubsidyInstanceItemInline(TabularInline):
    model = SubsidyInstanceItem
    extra = 1


class SubsidyInstanceAdmin(ModelAdmin):
    list_display = (
        "farmer",
        "subsidy_program",
        "redemption_date",
        "redemption_location",
        "get_total_subsidized_value",
    )
    list_filter = ("subsidy_program", "redemption_date")
    search_fields = ("farmer__name", "subsidy_program__title")
    inlines = [SubsidyInstanceItemInline]

    def get_total_subsidized_value(self, obj):
        return f"₦{obj.subsidized_value:.2f}"

    get_total_subsidized_value.short_description = "Total Subsidized Value"


class SubsidyInstanceItemAdmin(ModelAdmin):
    list_display = (
        "subsidy_instance",
        "subsidized_item",
        "quantity",
        "get_subsidized_value",
    )
    list_filter = ("subsidy_instance__subsidy_program", "subsidized_item__item_type")
    search_fields = ("subsidy_instance__farmer__name", "subsidized_item__item_name")

    def get_subsidized_value(self, obj):
        return f"₦{obj.subsidized_value:.2f}"

    get_subsidized_value.short_description = "Subsidized Value"


admin.site.register(SubsidizedItem, SubsidizedItemAdmin)
admin.site.register(SubsidyInstance, SubsidyInstanceAdmin)
admin.site.register(SubsidyInstanceItem, SubsidyInstanceItemAdmin)
