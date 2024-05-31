from django.contrib import admin

from market.models import Commodity, ContactPerson, Market, MarketCommodityPrice

# Register your models here.

admin.site.register(ContactPerson)
admin.site.register(Commodity)
admin.site.register(MarketCommodityPrice)
admin.site.register(Market)
