from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from market.models import (
    ContactPerson,
    Market,
    MarketDay,
    MarketPaymentMethod,
    Produce,
    ProducePrice,
)

# Register your models here.


@admin.register(Produce)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "local_name", "unit")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", "local_name")}


class IsMarketDayFilter(admin.SimpleListFilter):
    title = "Is Market Day"  # Filter label in the admin panel
    parameter_name = "is_market_day"  # Query parameter name

    def lookups(self, request, model_admin):
        """
        Defines the filter options that will appear in the admin panel filter
        """
        return (
            ("yes", "Yes"),
            ("no", "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(
                id__in=[market.id for market in queryset if market.is_market_day]
            )
        if self.value() == "no":
            return queryset.filter(
                id__in=[market.id for market in queryset if not market.is_market_day]
            )


@admin.register(Market)
class MarketAdmin(ModelAdmin):
    list_display = (
        "name",
        "custom_region",
        "custom_subregion",
        "last_market_day",
        "market_frequency",
        "next_market_day",
        "is_market_day",
        "number_of_vendors",
        "contact_person",
        "is_active",
    )
    autocomplete_fields = ("state", "local_govt")
    prepopulated_fields = {"slug": ("name", "state", "local_govt")}
    readonly_fields = ("next_market_day", "is_market_day")
    search_fields = ("name__istartswith",)
    list_filter = (IsMarketDayFilter,)

    def custom_region(self, market: Market):
        if market.state:
            return str(market.state).split(" ")[0]
        return market.state

    def custom_subregion(self, market: Market):
        if market.local_govt:
            return f"{str(market.local_govt).split(',')[0]}"
        return market.local_govt


@admin.register(ContactPerson)
class ContactPersonAdmin(ModelAdmin):
    list_display = (
        "fullname",
        "phone",
        "email",
        "role",
    )
    list_filter = ("role",)


class ProducePriceInline(TabularInline):
    model = ProducePrice
    extra = 1


@admin.register(MarketDay)
class MarketDayAdmin(ModelAdmin):
    list_display = ("market", "date")
    list_select_related = ("market",)
    list_filter = ("date",)

    inlines = [ProducePriceInline]


@admin.register(ProducePrice)
class ProductPriceAdmin(ModelAdmin):
    list_display = ("produce", "market_day", "price")
    list_select_related = ("produce", "market_day")
    list_filter = ("produce", "market_day")


@admin.register(MarketPaymentMethod)
class MarketPaymentMethodAdmin(ModelAdmin):
    list_display = ("market", "payment_method", "description")
    list_filter = ("payment_method",)
    list_select_related = ("market",)
    autocomplete_fields = ("market",)
