from django.db.models.signals import post_save
from django.dispatch import receiver

from market.models import ProducePrice


@receiver(post_save, sender=ProducePrice)
def update_last_market_day(sender, instance, created, **kwargs):
    if created:
        market_day = instance.market_day
        market = market_day.market

        if market_day.date > market.last_market_day:
            market.last_market_day = market_day.date
            market.save()

            # Invalidate the cached_property for the market
            if hasattr(market, "_next_market_day_cache"):
                del market._next_market_day_cache
