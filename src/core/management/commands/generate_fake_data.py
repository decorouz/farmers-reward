import random

from django.core.management.base import BaseCommand
from faker import Faker

from farmers.models import (
    Badge,
    CultivatedCrop,
    CultivatedField,
    CultivatedFieldHistory,
    Farmer,
    FarmersCooperative,
    FarmersMarketTransaction,
    FieldExtensionOfficer,
    Shock,
    UserBadge,
)
from market.models import ContactPerson, Market, MarketProduct, PaymentMethod, Product
from subsidy.models import (
    Agrochemical,
    Fertilizer,
    InputPriceHistory,
    Mechanization,
    Seed,
    SubsidizedItem,
    SubsidyInstance,
    SubsidyProgram,
    SubsidyRate,
)

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for the models"

    def handle(self, *args, **kwargs):
        self.generate_market_data()
        self.generate_farmers_cooperative()
        self.generate_field_extension_officers()
        self.generate_farmers()
        self.generate_cultivated_fields()
        self.generate_cultivated_field_history()
        self.generate_cultivated_crops()
        self.generate_farmers_market_transactions()
        self.generate_badges()
        self.generate_user_badges()
        # self.generate_subsidy_data()

    def generate_market_data(self):
        for _ in range(10):
            contact_person = ContactPerson.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone_number=fake.phone_number(),
            )
            market = Market.objects.create(
                name=fake.company(),
                display_address=fake.address(),
                contact_person=contact_person,
                market_day_interval=random.randint(1, 7),
                reference_mkt_date=fake.date(),
                slug=fake.slug(),
            )
            product = Product.objects.create(
                name=fake.word(),
                local_name=fake.word(),
                slug=fake.slug(),
            )
            payment_method = PaymentMethod.objects.create(
                name=random.randint(1, 6),
            )
            MarketProduct.objects.create(
                market=market,
                product=product,
                price=random.uniform(1.0, 100.0),
                mkt_date=fake.date(),
            )
            market.accepted_payment_methods.add(payment_method)

    def generate_farmers_cooperative(self):
        for _ in range(10):
            FarmersCooperative.objects.create(
                name=fake.company(),
                chairman=fake.name(),
                location=fake.address(),
                phone_number=fake.phone_number(),
                description=fake.text(),
                registration_number=random.randint(100000, 999999),
                verification_status=random.choice([True, False]),
                number_of_members=random.randint(10, 100),
                blacklisted=random.choice([True, False]),
            )

    def generate_field_extension_officers(self):
        for _ in range(10):
            FieldExtensionOfficer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                gender=random.choice(["Male", "Female"]),
                date_of_birth=fake.date_of_birth(),
                # age=random.randint(25, 60),
                education=random.randint(1, 5),
                # state_of_origin=fake.state(),
                # state_of_residence=fake.state(),
                phone_number=fake.phone_number(),
                slug=fake.slug(),
            )

    def generate_farmers(self):
        for _ in range(50):
            Farmer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=random.choice(["Male", "Female"]),
                date_of_birth=fake.date_of_birth(),
                # age=random.randint(18, 70),
                education=random.randint(1, 5),
                # state_of_origin=fake.state(),
                # state_of_residence=fake.state(),
                phone_number=fake.phone_number(),
                cooperative_society=random.choice(FarmersCooperative.objects.all()),
                field_extension_officer=random.choice(
                    FieldExtensionOfficer.objects.all()
                ),
                category_type=random.choice(["Small", "Medium", "Large"]),
                agricultural_activities=random.randint(1, 3),
                farmsize=random.uniform(1.0, 100.0),
                verification_status=random.choice([True, False]),
                verification_date=fake.date_this_year(),
                slug=fake.slug(),
            )

    def generate_cultivated_fields(self):
        for _ in range(50):
            CultivatedField.objects.create(
                farmer=random.choice(Farmer.objects.all()),
                field_size=random.uniform(1.0, 100.0),
                town=fake.city(),
                # region=fake.state(),
                # sub_region=fake.state(),
                # country=random.choice(["Nigeria"]),
                latitude=fake.latitude(),
                logitude=fake.longitude(),
                soil_type=random.choice(["Clay", "Sandy", "Loamy", "Silt"]),
                soil_test_date=fake.date_this_year(),
                test_results_file=fake.file_name(),
                slug=fake.slug(),
            )

    def generate_cultivated_field_history(self):
        for _ in range(5):
            CultivatedFieldHistory.objects.create(
                cultivated_field=random.choice(CultivatedField.objects.all()),
                farming_system=random.choice(
                    [
                        "MONO",
                        "MULTI",
                        "MIXED",
                    ]
                ),
                year=fake.year(),
                primary_crop_type=fake.word(),
            )

    def generate_cultivated_crops(self):
        for _ in range(50):
            CultivatedCrop.objects.create(
                field=random.choice(CultivatedField.objects.all()),
                crop=fake.word(),
                planting_date=fake.date_this_year(),
                harvest_date=fake.date_this_year(),
                yield_amount=random.uniform(1.0, 100.0),
            )

    def generate_farmers_market_transactions(self):
        for _ in range(50):
            product = Product.objects.create(
                name=fake.word(),
                local_name=fake.word(),
                slug=fake.slug(),
            )
            FarmersMarketTransaction.objects.create(
                farmer=random.choice(Farmer.objects.all()),
                market=random.choice(Market.objects.all()),
                produce=product,
                quantity=random.uniform(1.0, 100.0),
                created_on=fake.date_this_year(),
                points_earned=random.randint(1, 100),
            )

    def generate_badges(self):
        for _ in range(10):
            Badge.objects.create(
                name=random.choice(["B", "S", "G"]),
                image_thumbnail=fake.image_url(),
                points_required=random.randint(1, 100),
            )

    def generate_user_badges(self):
        for _ in range(50):
            UserBadge.objects.create(
                farmer=random.choice(Farmer.objects.all()),
                badge=random.choice(Badge.objects.all()),
                earned_on=fake.date_this_year(),
            )

    # def generate_subsidy_data(self):
    #     for _ in range(10):
    #         SubsidyProgram.objects.create(
    #             title=fake.word(),
    #             objective=fake.text(),
    #             slug=fake.slug(),
    #             program_adminstrator=random.choice(["STATE", "NATIONAL"]),
    #             start_date=fake.date_this_year(),
    #             end_date=fake.date_this_year(),
    #         )
    #         SubsidizedItem.objects.create(
    #             type=random.choice(["SEED", "FERT", "MECH"]),
    #         )
    #         SubsidyRate.objects.create(
    #             item=random.choice(SubsidizedItem.objects.all()),
    #             rate=random.uniform(1.0, 100.0),
    #         )
    #         SubsidyInstance.objects.create(
    #             program=random.choice(SubsidyProgram.objects.all()),
    #             item=random.choice(SubsidizedItem.objects.all()),
    #             quantity=random.uniform(1.0, 100.0),
    #             date=fake.date_this_year(),
    #         )
    #         Agrochemical.objects.create(
    #             name=fake.word(),
    #             description=fake.text(),
    #         )
    #         Fertilizer.objects.create(
    #             name=fake.word(),
    #             description=fake.text(),
    #         )
    #         Seed.objects.create(
    #             name=fake.word(),
    #             description=fake.text(),
    #         )
    #         Mechanization.objects.create(
    #             name=fake.word(),
    #             description=fake.text(),
    #         )
    #         InputPriceHistory.objects.create(
    #             item=random.choice(SubsidizedItem.objects.all()),
    #             price=random.uniform(1.0, 100.0),
    #             date=fake.date_this_year(),
    #         )
