# Create your views here.

# Veiw list of all markets
# View market details
# View list of all commodities
# View product details
# Search market by local govt area, state, town, city, market name, next market date
# View list of all market product prices
# View list of all contact persons
#
from django.shortcuts import render

from market.models import Market

# def home_page(request):
#     """Return the top three markets"""
#     markets = Market.objects.all()[0:4]
#     return render(request, "core/home.html", {"markets": markets})
