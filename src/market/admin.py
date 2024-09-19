from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from market.models import ContactPerson, Market, MarketDay, Product, ProductPrice

# Register your models here.


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "local_name", "unit")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", "local_name")}


@admin.register(Market)
class MarketAdmin(ModelAdmin):
    list_display = (
        "name",
        "custom_region",
        "custom_subregion",
        "reference_mkt_date",
        "frequency",
        "next_marketdate",
        "is_market_day",
        "number_of_vendors",
        "contact_person",
        "is_active",
    )
    autocomplete_fields = ("state", "local_govt")
    prepopulated_fields = {"slug": ("name", "state", "local_govt")}
    search_fields = ("name__istartswith",)

    def custom_region(self, market: Market):
        if market.state:
            return str(market.state).split(" ")[0]
        return market.state

    def custom_subregion(self, market: Market):
        if market.local_govt:
            return f"{str(market.local_govt).split(',')[0]}"
        return market.local_govt

    def next_marketdate(self, market):
        from datetime import date, timedelta

        if market.reference_mkt_date and market.frequency:
            while market.reference_mkt_date <= date.today():
                market.reference_mkt_date += timedelta(days=market.frequency)
            return market.reference_mkt_date
        return None


@admin.register(ContactPerson)
class ContactPersonAdmin(ModelAdmin):
    list_display = (
        "fullname",
        "phone",
        "email",
        "role",
    )
    list_filter = ("role",)


class ProductPriceInline(TabularInline):
    model = ProductPrice
    extra = 1


@admin.register(MarketDay)
class MarketDayAdmin(ModelAdmin):
    list_display = ("market", "mkt_date")
    list_select_related = ("market",)
    list_filter = ("mkt_date",)

    inlines = [ProductPriceInline]


# @admin.register(ProductPrice)
# class ProductPriceAdmin(ModelAdmin):
#     list_display = ("product", "market_day", "price")
#     list_select_related = ("product", "market_day")
