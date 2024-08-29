from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from market.models import ContactPerson, Market, MarketProduct, PaymentMethod, Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "local_name", "unit")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name", "local_name")}


admin.site.register(PaymentMethod)


@admin.register(Market)
class MarketAdmin(ModelAdmin):
    list_display = (
        "name",
        "custom_region",
        "custom_subregion",
        "reference_mkt_date",
        "market_day_interval",
        "next_marketdate",
        "number_of_vendors",
        "contact_person",
        "is_active",
    )
    autocomplete_fields = ("region", "sub_region")
    prepopulated_fields = {"slug": ("name", "region", "sub_region")}
    search_fields = ("name__istartswith",)

    def custom_region(self, market: Market):
        if market.region:
            return str(market.region).split(" ")[0]
        return market.region

    def custom_subregion(self, market: Market):
        if market.sub_region:
            return f"{str(market.sub_region).split(',')[0]}"
        return market.sub_region

    def next_marketdate(self, market):
        from datetime import date, timedelta

        if market.reference_mkt_date and market.market_day_interval:
            while market.reference_mkt_date <= date.today():
                market.reference_mkt_date += timedelta(days=market.market_day_interval)
            return market.reference_mkt_date
        return None


@admin.register(MarketProduct)
class MarketProductAdmin(ModelAdmin):
    autocomplete_fields = ("market", "product")
    list_display = (
        "market",
        "product",
        "price",
        "mkt_date",
    )
    list_select_related = ("market", "product")


@admin.register(ContactPerson)
class ContactPersonAdmin(ModelAdmin):
    list_display = (
        "fullname",
        "phone",
        "email",
        "role",
    )
    list_filter = ("role",)
