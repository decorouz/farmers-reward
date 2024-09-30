from cities_light.models import Country  # Import models for state and LGA
from cities_light.models import Region, SubRegion
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from farmers.models import AgroVendor, Farmer, FieldExtensionOfficer

fake = Faker()

states_info = [
    ("Kano", "Kano Municipal"),
    ("Lagos", "Lagos Island"),
    ("Oyo", "Ibadan"),
    ("Kwara", "Ilorin West"),
    ("Ekiti", "Ado Ekiti"),
]


class Command(BaseCommand):
    help = "Populate the database with 5 unique records for each model"

    def handle(self, *args, **options):
        self.populate_agro_vendors()
        self.populate_field_extension_officers()
        self.populate_farmers()

    def populate_agro_vendors(self):
        for _ in range(5):
            country, created = Country.objects.get_or_create(name="Nigeria", code2="NG")
            state_name, lga_name = fake.random_element(elements=states_info)
            state = Region.objects.get(name=state_name, country=country)
            lga = SubRegion.objects.get(name=lga_name, region=state, country=country)

            AgroVendor.objects.create(
                name=fake.company(),
                phone_number=f"080{fake.numerify('########')}",
                email=fake.email(),
                street=fake.street_address(),
                state=state,
                country_id=1,  # Replace with actual country ID
                lga=lga,
            )

    def populate_field_extension_officers(self):
        for _ in range(5):
            country, created = Country.objects.get_or_create(name="Nigeria", code2="NG")
            state_name, lga_name = fake.random_element(elements=states_info)
            state = Region.objects.get(name=state_name, country=country)
            lga = SubRegion.objects.get(
                name=lga_name, region=state, country=country
            )  # Randomly choose a state of origin

            FieldExtensionOfficer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=f"080{fake.numerify('########')}",
                email=fake.email(),
                street=fake.street_address(),
                state=state,
                country_id=1,
                lga=lga,
                state_of_origin=state,
                gender=fake.random_element(elements=("M", "F")),
                education=fake.random_int(min=1, max=5),
                means_of_identification=fake.random_element(
                    elements=("ND", "IP", "DL")
                ),
                identification_number=fake.numerify("########"),
                slug=slugify(fake.first_name() + "-" + fake.last_name()),
            )

    def populate_farmers(self):
        for _ in range(5):
            country, created = Country.objects.get_or_create(name="Nigeria", code2="NG")
            state_name, lga_name = fake.random_element(elements=states_info)
            state = Region.objects.get(name=state_name, country=country)
            lga = SubRegion.objects.get(
                name=lga_name, region=state, country=country
            )  # Randomly choose a state of origin

            Farmer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=f"080{fake.numerify('########')}",
                email=fake.email(),
                street=fake.street_address(),
                state=state,
                country_id=1,
                lga=lga,
                state_of_origin=state,
                gender=fake.random_element(elements=("M", "F")),
                education=fake.random_int(min=1, max=5),
                means_of_identification=fake.random_element(
                    elements=("ND", "IP", "DL")
                ),
                identification_number=fake.numerify("########"),
                slug=slugify(fake.first_name() + "-" + fake.last_name()),
                agricultural_activities=fake.random_int(min=1, max=3),
                category_type=fake.random_element(elements=("SH", "MC")),
                farmsize=fake.random_element(elements=("<1", "1-3", "3-5", ">5")),
            )
