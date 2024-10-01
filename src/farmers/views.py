from django.shortcuts import render

from farmers.models import FarmersInputTransaction, FarmersMarketTransaction

from .filters import TransactionFilter


def market_transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=FarmersMarketTransaction.objects.all().select_related(
            "farmer", "market", "produce"
        ),
    )
    context = {
        "filter": transaction_filter,
    }
    return render(request, "farmers/transactions-list.html", context)


# Farmers onboarding
# Field extension officer onboarding
# Farmers cooperative onboarding
# Upon completion of the onboarding process, the farmer should be assigned to a field extension officer and a unique number should be generated for the farmer.
