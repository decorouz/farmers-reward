import random
from datetime import timedelta

from cities_light.models import Country, Region, SubRegion
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from market.models import (
    Address,
    ContactPerson,
    Market,
    MarketDay,
    PaymentMethod,
    Produce,
    ProducePrice,
)


class Command(BaseCommand):
    help = "Populates the database with 10 records for Produce, Market, MarketDay, and ProducePrice models"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Step 1: Create Country, Region, and SubRegion
            country, created = Country.objects.get_or_create(name="Nigeria", code2="NG")
            states_info = [
                ("Kano", "Kano Municipal"),
                ("Lagos", "Lagos Island"),
                ("Oyo", "Ibadan"),
                ("Kwara", "Ilorin West"),
                ("Ekiti", "Ado Ekiti"),
            ]

            regions = {}
            for state, subregion in states_info:
                region, created = Region.objects.get_or_create(
                    name=state, country=country
                )
                subregion_obj, created = SubRegion.objects.get_or_create(
                    name=subregion, region=region, country=country
                )
                regions[state] = (region, subregion_obj)

            # Step 2: Create 5 different ContactPerson records
            contact_people = []
            for i in range(5):
                contact_person = ContactPerson.objects.create(
                    first_name=f"Person{i+1}",
                    last_name=f"Last{i+1}",
                    email=f"person{i+1}@example.com",
                    phonenumber=f"0906959232{i}",
                    role=random.choice(["MA", "ML"]),
                    is_active=True,
                )
                contact_people.append(contact_person)

            # Step 4: Create 5 unique Produce records (no duplicate names)
            produce_items = []
            produce_data = [
                {"name": Produce.ProduceChoices.WHEAT, "local_name": "Wheat"},
                {"name": Produce.ProduceChoices.MILLET, "local_name": "Millet"},
                {"name": Produce.ProduceChoices.GINGER, "local_name": "Ginger"},
                {"name": Produce.ProduceChoices.PADDY_RICE, "local_name": "Paddy Rice"},
                {
                    "name": Produce.ProduceChoices.BROWN_COWPEA,
                    "local_name": "Brown Cowpea",
                },
                {
                    "name": Produce.ProduceChoices.WHITE_COWPEA,
                    "local_name": "White Cowpea",
                },
            ]

            # Iterate over the data and create Produce objects
            for produce in produce_data:
                produce, created = Produce.objects.get_or_create(
                    name=produce["name"],
                    defaults={
                        "slug": slugify(produce["name"]),
                        "local_name": produce["local_name"],
                        "unit": Produce.UnitChoices.BAG,  # Default unit for now
                    },
                )

                produce_items.append(produce)

            # Create 5 different Payment methods
            payment_methods = []
            paymethod_data = [
                {"type": PaymentMethod.PaymentMethodChoice.CREDIT_CARD},
                {"type": PaymentMethod.PaymentMethodChoice.MOBILE_MONEY},
                {"type": PaymentMethod.PaymentMethodChoice.BANK_TRANSFER},
                {"type": PaymentMethod.PaymentMethodChoice.POINT_OF_SALE},
                {"type": PaymentMethod.PaymentMethodChoice.CASH},
            ]

            # Iterate over the data and create Produce objects
            for payment in paymethod_data:
                obj, created = PaymentMethod.objects.get_or_create(
                    type=payment["type"],
                )

                payment_methods.append(obj)

            # Step 3: Create 5 different Market records with unique ContactPerson for each Market
            markets = []

            for i in range(5):
                market_name = f"Market{i+1}"
                market_slug = self.get_unique_slug(Market, market_name)

                contact_person = contact_people.pop(0)
                market = Market.objects.create(
                    name=market_name,
                    description=f"Description for Market{i+1}",
                    number_of_vendors=random.randint(50, 200),
                    operating_hours="8:00 AM - 5:00 PM",
                    market_frequency=random.randint(1, 6),
                    last_market_day=timezone.now()
                    - timedelta(days=random.randint(1, 10)),
                    slug=market_slug,  # Unique slug for each market
                    contact_person=contact_person,
                    is_active=True,
                )
                # Use set() to assign payment_methods and produce_items
                market.payment_methods.set(payment_methods)
                market.produce_items.set(produce_items)
                markets.append(market)

            # Step 4: Create 5 different Address records
            addresses = []
            for state, (region, subregion_obj) in regions.items():
                market = markets.pop(0)
                address = Address.objects.create(
                    street=f"{state} Street",
                    town=f"{state} Town",
                    local_govt=subregion_obj,
                    state=region,
                    country=country,
                    latitude=random.uniform(1.5, 1.9),
                    longitude=random.uniform(2.5, 4.9),
                    market=market,
                )
                addresses.append(address)

            # Step 5: Create 5 different MarketDay records
            market_days = []
            for market in markets:
                market_day = MarketDay.objects.create(
                    market=market,
                    events=f"Market Day events for {market.name}",
                    date=timezone.now() - timedelta(days=random.randint(0, 10)),
                )
                market_days.append(market_day)

            # Step 6: Create ProducePrice records for each produce and market day combination
            for i in range(len(markets)):
                ProducePrice.objects.create(
                    produce=produce_items[
                        i % len(produce_items)
                    ],  # Rotate through produce
                    market_day=market_days[i],
                    price=random.uniform(1000.00, 5000.00),
                )

        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with 5 records.")
        )

    def get_unique_slug(self, model_class, base_text):
        """
        Generates a unique slug for the given model based on the base text.
        If a slug already exists, it appends a number to make it unique.
        """
        slug = slugify(base_text)
        unique_slug = slug
        counter = 1
        while model_class.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug
