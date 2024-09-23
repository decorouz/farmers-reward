import random
from datetime import timedelta

from cities_light.models import Country, Region, SubRegion
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from market.models import ContactPerson, Market, MarketDay, Produce, ProducePrice


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

            # Step 2: Create 10 different ContactPerson records
            contact_people = []
            for i in range(10):
                contact_person = ContactPerson.objects.create(
                    first_name=f"Person{i+1}",
                    last_name=f"Last{i+1}",
                    email=f"person{i+1}@example.com",
                    phone=f"0906959232{i}",
                    role="extension_agent",
                    is_active=True,
                )
                contact_people.append(contact_person)

            # Step 3: Create 10 different Market records with unique ContactPerson for each Market
            markets = []
            for state, (region, subregion_obj) in regions.items():
                for i in range(2):
                    market_name = f"Market{i+1}{region}"
                    market_slug = self.get_unique_slug(Market, market_name)

                    contact_person = contact_people.pop(0)
                    market = Market.objects.create(
                        name=market_name,
                        slug=market_slug,  # Unique slug for each market
                        description=f"Description for Market{i+1}",
                        number_of_vendors=random.randint(50, 200),
                        operating_hours="8:00 AM - 5:00 PM",
                        market_frequency=random.randint(1, 7),
                        last_market_day=timezone.now()
                        - timedelta(days=random.randint(1, 10)),
                        contact_person=contact_person,
                        is_active=True,
                        street_address=f"{i+1} Example St",
                        town=f"{i+1} City",
                        local_govt=subregion_obj,
                        state=region,
                        country=country,
                        latitude=12.0 + i,  # Varying latitude
                        longitude=8.0 + i,  # Varying longitude
                    )
                markets.append(market)

            # Step 4: Create 10 unique Produce records (no duplicate names)
            produce_items = []
            produce_names = [
                Produce.ProduceChoices.WHEAT,
                Produce.ProduceChoices.MILLET,
                Produce.ProduceChoices.GINGER,
                Produce.ProduceChoices.PADDY_RICE,
                Produce.ProduceChoices.BROWN_COWPEA,
                Produce.ProduceChoices.WHITE_COWPEA,
                Produce.ProduceChoices.WHITE_MAIZE,
                Produce.ProduceChoices.YELLOW_MAIZE,
                Produce.ProduceChoices.CASSAVA,
                Produce.ProduceChoices.ONION,
            ]
            for i, produce_name in enumerate(produce_names):
                produce_slug = self.get_unique_slug(Produce, produce_name)

                # Check if the Produce already exists to avoid duplicates
                produce, created = Produce.objects.get_or_create(
                    name=produce_name,
                    defaults={
                        "slug": produce_slug,
                        "local_name": f"Local {produce_name}",
                        "unit": Produce.UnitChoices.KG,
                    },
                )

                produce_items.append(produce)

            # Step 5: Create 10 different MarketDay records
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
            self.style.SUCCESS("Successfully populated the database with 10 records.")
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
