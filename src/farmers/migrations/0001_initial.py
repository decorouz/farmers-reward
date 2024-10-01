# Generated by Django 5.1.1 on 2024-10-01 23:23

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("market", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AgroVendor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=14, null=True, region=None, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("street", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(max_length=100)),
                ("verification_status", models.BooleanField(default=False)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.country",
                    ),
                ),
                (
                    "lga",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.subregion",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.region",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FieldExtensionOfficer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=14, null=True, region=None, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("street", models.CharField(blank=True, max_length=255, null=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        default=datetime.date(1990, 12, 29), verbose_name="Birthday"
                    ),
                ),
                (
                    "education",
                    models.IntegerField(
                        choices=[
                            (1, "None or did not complete primary school"),
                            (2, "Completed primary school"),
                            (3, "Completed secondary school"),
                            (4, "Completed higher education"),
                            (5, "Religious or informal education"),
                            (888, "Don't know"),
                            (999, "Refused"),
                        ]
                    ),
                ),
                (
                    "means_of_identification",
                    models.CharField(
                        choices=[
                            ("ND", "National ID"),
                            ("IP", "International Passport"),
                            ("DL", "Driver's License"),
                        ],
                        default="ND",
                        max_length=2,
                    ),
                ),
                (
                    "identification_number",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("blacklisted", models.BooleanField(default=False)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "affiliation",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.country",
                    ),
                ),
                (
                    "lga",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.subregion",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.region",
                    ),
                ),
                (
                    "state_of_origin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.region",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Farmer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=14, null=True, region=None, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("street", models.CharField(blank=True, max_length=255, null=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=1
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        default=datetime.date(1990, 12, 29), verbose_name="Birthday"
                    ),
                ),
                (
                    "education",
                    models.IntegerField(
                        choices=[
                            (1, "None or did not complete primary school"),
                            (2, "Completed primary school"),
                            (3, "Completed secondary school"),
                            (4, "Completed higher education"),
                            (5, "Religious or informal education"),
                            (888, "Don't know"),
                            (999, "Refused"),
                        ]
                    ),
                ),
                (
                    "means_of_identification",
                    models.CharField(
                        choices=[
                            ("ND", "National ID"),
                            ("IP", "International Passport"),
                            ("DL", "Driver's License"),
                        ],
                        default="ND",
                        max_length=2,
                    ),
                ),
                (
                    "identification_number",
                    models.CharField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("blacklisted", models.BooleanField(default=False)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "category_type",
                    models.CharField(
                        choices=[("SH", "Smallholder"), ("MC", "Commercial")],
                        default="MC",
                        max_length=3,
                    ),
                ),
                (
                    "agricultural_activities",
                    models.IntegerField(
                        choices=[
                            (1, "Crop Producer"),
                            (2, "Livestock Producer"),
                            (3, "Crop and Livestock Producer"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "farmsize",
                    models.CharField(
                        choices=[
                            ("<1", "<1 Hectare"),
                            ("1-3", "1-3 Hectares"),
                            ("3-5", "3-5 Hectares"),
                            (">5", ">5 Hectares"),
                        ],
                        default="1-3",
                        max_length=3,
                    ),
                ),
                (
                    "has_market_transaction",
                    models.BooleanField(default=False, editable=False),
                ),
                (
                    "has_input_transaction",
                    models.BooleanField(default=False, editable=False),
                ),
                ("is_verified", models.BooleanField(default=False, editable=False)),
                (
                    "earned_points",
                    models.IntegerField(
                        default=0,
                        editable=False,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.country",
                    ),
                ),
                (
                    "lga",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.subregion",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.region",
                    ),
                ),
                (
                    "state_of_origin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="cities_light.region",
                    ),
                ),
                (
                    "field_extension_officer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="farmer",
                        to="farmers.fieldextensionofficer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FarmersInputTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "receipt_number",
                    models.CharField(default="000000", max_length=255, unique=True),
                ),
                (
                    "receipt_verification_date",
                    models.DateField(default=django.utils.timezone.now),
                ),
                (
                    "points_earned",
                    models.IntegerField(
                        editable=False,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "farmer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="input_transaction",
                        to="farmers.farmer",
                    ),
                ),
                (
                    "market",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="input_transaction",
                        to="market.market",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="input_transaction",
                        to="farmers.agrovendor",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("receipt_number", "farmer"),
                        name="unique_receipt_identifier",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="FarmersMarketTransaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField()),
                ("transaction_date", models.DateField()),
                (
                    "points_earned",
                    models.IntegerField(
                        editable=False,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "farmer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mkt_transaction",
                        to="farmers.farmer",
                    ),
                ),
                (
                    "market",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mkt_transaction",
                        to="market.market",
                    ),
                ),
                (
                    "produce",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="market.produce"
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("produce", "farmer", "market", "transaction_date"),
                        name="unique_mkt_transaction",
                    )
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="fieldextensionofficer",
            constraint=models.UniqueConstraint(
                fields=("identification_number", "phone_number"),
                name="unique_identification_number",
            ),
        ),
        migrations.AddConstraint(
            model_name="farmer",
            constraint=models.UniqueConstraint(
                fields=("identification_number", "phone_number"),
                name="farmer_unique_id",
            ),
        ),
    ]
