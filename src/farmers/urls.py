from django.urls import path

from . import views

urlpatterns = [
    path("transactions/", views.market_transaction_list, name="transactions-list")
]
