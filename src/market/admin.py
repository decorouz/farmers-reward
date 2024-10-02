from ast import Add

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from market.models import (
    Address,
    ContactPerson,
    Market,
    MarketDay,
    PaymentMethod,
    Produce,
    ProducePrice,
)

# Register your models here.


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = (
        "street",
        "town",
        "local_govt",
        "state",
        "latitude",
        "longitude",
    )
    search_fields = (
        "local_govt",
        "state",
    )
    autocomplete_fields = ("local_govt", "state", "country")
    list_filter = ("state", "local_govt")
    list_select_related = ("state", "local_govt", "country")

    def custom_region(self, address: Address):
        if address.state:
            return str(address.state).split(" ")[0]
        return address.state

    def custom_subregion(self, address: Address):
        if address.local_govt:
            return f"{str(address.local_govt).split(',')[0]}"
        return address.local_govt


@admin.register(Produce)
class ProductAdmin(ModelAdmin):
    list_display = (
        "name",
        "local_name",
        # "category",
        "unit",
    )
    # list_filter = ("category",)


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
        "last_market_day",
        "market_frequency",
        "next_market_day",
        "is_market_day",
        "number_of_vendors",
        "contact_person",
        "is_active",
    )
    readonly_fields = ("next_market_day", "is_market_day")
    search_fields = ("name__istartswith",)
    list_filter = (IsMarketDayFilter,)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactPerson)
class ContactPersonAdmin(ModelAdmin):
    list_display = (
        "fullname",
        "phone_number",
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
    list_display = (
        "produce",
        "produce__category",
        "market_day",
        "market_day__market",
        "price_type",
        "price",
        "produce__unit",
    )
    list_select_related = ("produce", "market_day")
    list_filter = ("market_day", "price_type")


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ("type",)
    list_filter = ("type",)
