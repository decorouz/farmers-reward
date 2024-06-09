# Generated by Django 5.0.6 on 2024-06-09 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Commodity",
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
                    "crop_name",
                    models.CharField(
                        choices=[
                            ("wheat", "Wheat"),
                            ("corn", "Corn"),
                            ("rice", "Rice"),
                            ("soybean", "Soybean"),
                            ("cotton", "Cotton"),
                            ("barley", "Barley"),
                            ("oats", "Oats"),
                            ("sorghum", "Sorghum"),
                            ("millet", "Millet"),
                            ("potato", "Potato"),
                            ("sugar_beet", "Sugar Beet"),
                            ("cassava", "Cassava"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "commodities",
            },
        ),
        migrations.CreateModel(
            name="ContactPerson",
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
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("extension_agent", "Extension Agent"),
                            ("chairman", "Chairman"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Market",
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
                    "display_address",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "local_govt_area",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("town", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("state", models.CharField(blank=True, max_length=255, null=True)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("latitude", models.FloatField(blank=True, max_length=9, null=True)),
                ("longitude", models.FloatField(blank=True, max_length=9, null=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("number_of_vendors", models.IntegerField(default=0)),
                ("market_day_interval", models.SmallIntegerField(default=4)),
                (
                    "reference_mkt_date",
                    models.DateField(verbose_name="confirmed market date"),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MarketCommodityPrice",
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
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "market commodities",
                "verbose_name_plural": "market commodities",
            },
        ),
        migrations.CreateModel(
            name="PaymentMethod",
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
                    "name",
                    models.CharField(
                        choices=[
                            ("CH", "Cash"),
                            ("CC", "Credit Card"),
                            ("POS", "Point of Sale"),
                            ("ATM", "ATM Onsite"),
                            ("ATM_nearby", "ATM within 5 minutes walk"),
                            ("BT", "Bank Transfer"),
                        ],
                        default="CH",
                        max_length=255,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="commodity",
            constraint=models.UniqueConstraint(
                fields=("crop_name",), name="unique_crop_name"
            ),
        ),
        migrations.AddField(
            model_name="market",
            name="contact_person",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="markets",
                to="market.contactperson",
            ),
        ),
        migrations.AddField(
            model_name="marketcommodityprice",
            name="commodity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="market.commodity"
            ),
        ),
        migrations.AddField(
            model_name="marketcommodityprice",
            name="market",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="market.market"
            ),
        ),
        migrations.AddField(
            model_name="market",
            name="market_products",
            field=models.ManyToManyField(
                blank=True,
                related_name="markets",
                through="market.MarketCommodityPrice",
                to="market.commodity",
            ),
        ),
        migrations.AddField(
            model_name="market",
            name="accepted_payment_methods",
            field=models.ManyToManyField(
                blank=True, related_name="markets", to="market.paymentmethod"
            ),
        ),
        migrations.AddConstraint(
            model_name="marketcommodityprice",
            constraint=models.UniqueConstraint(
                fields=("commodity", "market", "date"), name="unique_item"
            ),
        ),
        migrations.AddConstraint(
            model_name="market",
            constraint=models.UniqueConstraint(
                fields=("name",), name="unique_market_name"
            ),
        ),
    ]
