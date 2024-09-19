# Generated by Django 5.1.1 on 2024-09-19 19:43

import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
import phonenumber_field.modelfields
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("farmers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Agrochemical",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("manufacturer", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "agrochemical_type",
                    models.CharField(
                        choices=[
                            ("PRE", "Pre Emergence Herbicide"),
                            ("POS", "Post Emergence Herbicide"),
                            ("PES", "Pesticide"),
                            ("INT", "Insecticide"),
                        ],
                        default="PRE",
                        max_length=3,
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(
                            (
                                "manufacturer__iexact",
                                django.db.models.functions.text.Lower("manufacturer"),
                            )
                        ),
                        fields=("manufacturer", "name", "agrochemical_type"),
                        name="unique_agrochemical_manufacturer_type",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="Fertilizer",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("manufacturer", models.CharField(max_length=100)),
                (
                    "fertilizer_type",
                    models.CharField(
                        choices=[
                            ("NPK", "Npk"),
                            ("UREA", "Urea"),
                            ("SSP", "Single Super Phosphate"),
                            ("MOP", "Muriate of Potash"),
                            ("OTHER", "Others"),
                        ],
                        default="NPK",
                        max_length=5,
                    ),
                ),
                (
                    "fertilizer_blend",
                    models.CharField(
                        default="20:10:10",
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\d+:\\d+:\\d+$", "Invalid fertilizer blend format"
                            )
                        ],
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(
                            (
                                "manufacturer__iexact",
                                django.db.models.functions.text.Lower("manufacturer"),
                            )
                        ),
                        fields=("manufacturer", "fertilizer_type", "fertilizer_blend"),
                        name="unique_fertilizer",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="MechanizationOperation",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "operation_type",
                    models.CharField(
                        choices=[
                            ("PLOWING", "Plowing"),
                            ("HARVESTING", "Harvesting"),
                            ("PLANTING", "Planting"),
                            ("SPRAYING", "Spraying"),
                            ("TILLING", "Tilling"),
                            ("FERTILIZING", "Fertilizing"),
                            ("IRRIGATING", "Irrigating"),
                            ("OTHER", "Other"),
                        ],
                        default="PLOWING",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("operation_type",),
                        name="unique_mechanization_operation",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="Seed",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("seed_company", models.CharField(default="Seedco", max_length=100)),
                (
                    "crop",
                    models.CharField(
                        choices=[
                            ("MAIZE", "Maize"),
                            ("COWPEA", "Cowpea"),
                            ("SOYBEAN", "Soybean"),
                            ("RICE", "Rice"),
                            ("SORGHUM", "Sorghum"),
                            ("MILLET", "Millet"),
                            ("GROUNDNUT", "Groundnut"),
                            ("COTTON", "Cotton"),
                            ("SESAME", "Sesame"),
                            ("YAM", "Yam"),
                            ("CASSAVA", "Cassava"),
                            ("TOMATO", "Tomatoe"),
                            ("PEPPER", "Pepper"),
                            ("OTHER", "Others"),
                        ],
                        default="MAIZE",
                        max_length=20,
                    ),
                ),
                (
                    "seed_variety",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("gmo", models.BooleanField(default=False)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(
                            (
                                "seed_variety__iexact",
                                django.db.models.functions.text.Lower("seed_variety"),
                            )
                        ),
                        fields=("seed_company", "crop", "seed_variety"),
                        name="unique_seed",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="SubsidizedItem",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "item_type",
                    models.CharField(
                        choices=[
                            ("FERTILIZER", "Fertilizer"),
                            ("SEED", "Seed"),
                            ("AGROCHEMICAL", "Agrochemical"),
                            ("MECHANIZATION", "Mechanization"),
                        ],
                        max_length=20,
                    ),
                ),
                ("item_name", models.CharField(max_length=255)),
                (
                    "item_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("kg", "kilogram"),
                            ("50kg", "50 kilogram"),
                            ("ltr", "liter"),
                            ("ha", "hectare"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "agrochemical",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subsidy.agrochemical",
                    ),
                ),
                (
                    "fertilizer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subsidy.fertilizer",
                    ),
                ),
                (
                    "mechanization_operation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subsidy.mechanizationoperation",
                    ),
                ),
                (
                    "seed",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subsidy.seed",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubsidyInstance",
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
                ("redemption_date", models.DateField(auto_now_add=True)),
                (
                    "redemption_location",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "farmer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="subsidy_instances",
                        to="farmers.farmer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubsidyInstanceItem",
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
                    "quantity",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "subsidized_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subsidy_instance_items",
                        to="subsidy.subsidizeditem",
                    ),
                ),
                (
                    "subsidy_instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subsidy_instance_items",
                        to="subsidy.subsidyinstance",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubsidyProgram",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=14, null=True, region=None, unique=True
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("implementation_details", models.TextField(blank=True, null=True)),
                (
                    "program_sponsor",
                    models.CharField(default="Federal Government", max_length=255),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[("STATE", "State"), ("NATIONAL", "National")],
                        default="NATIONAL",
                        max_length=10,
                    ),
                ),
                (
                    "current_num_of_beneficiaries",
                    models.SmallIntegerField(default=0, editable=False),
                ),
                (
                    "budget_in_naira",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=Decimal("7000000000.00"),
                        max_digits=40,
                        null=True,
                    ),
                ),
                ("start_date", models.DateField(auto_now_add=True)),
                ("end_date", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "rate",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cities_light.country",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cities_light.region",
                    ),
                ),
            ],
            options={
                "verbose_name": "Program",
                "verbose_name_plural": "Programs",
                "ordering": ["-start_date"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="subsidyinstance",
            name="subsidy_program",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subsidy_instances",
                to="subsidy.subsidyprogram",
            ),
        ),
        migrations.AddConstraint(
            model_name="subsidizeditem",
            constraint=models.UniqueConstraint(
                fields=("item_type", "item_name"), name="unique_subsidized_item"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="subsidyinstanceitem",
            unique_together={("subsidy_instance", "subsidized_item")},
        ),
        migrations.AddConstraint(
            model_name="subsidyinstance",
            constraint=models.UniqueConstraint(
                fields=("farmer", "subsidy_program"), name="unique_farmer_subsidy"
            ),
        ),
    ]
