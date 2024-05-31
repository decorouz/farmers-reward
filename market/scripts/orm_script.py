from django.utils import timezone

from market.models import Market


def run():
    market = Market()
    market.name = "Test Market"
    market.accepted_payment_method = Market.PaymentMethodChoices.CASH
    market.description = "Kara Ajasse Market"
    market.number_of_vendors = 4
    market.market_day_interval = 5
    market.reference_mkt_date = timezone.now().date()
    market.address = "Ajasse Kwara state"
    market.save()
