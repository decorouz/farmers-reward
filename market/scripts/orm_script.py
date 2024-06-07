from django.utils import timezone

from market.models import Market


def run():
    market = Market()
    market.name = "Test Market 2"
    market.latitude = 8.785262480072822
    market.longitude = 5.29353307490489
    market.number_of_vendors = 4
    market.market_day_interval = 5
    market.reference_mkt_date = timezone.now().date()

    market.save()
