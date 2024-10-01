import django_filters
from django import forms

from farmers.models import FarmersMarketTransaction
from market.models import Market, Produce


class TransactionFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(
        field_name="transaction_date",
        lookup_expr="gte",
        label="Date From",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    end_date = django_filters.DateFilter(
        field_name="transaction_date",
        lookup_expr="lte",
        label="Date To",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    produce = django_filters.ModelChoiceFilter(
        queryset=Produce.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = FarmersMarketTransaction
        fields = ("start_date", "end_date", "produce")
