# Generated by Django 5.1 on 2024-08-24 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0001_initial"),
        ("market", "0002_alter_product_name_alter_product_unit"),
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crop",
            fields=[
                (
                    "product_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="market.product",
                    ),
                ),
                ("variety", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("market.product",),
        ),
        migrations.RemoveField(
            model_name="cultivatedfieldhistory",
            name="pri_crop_harvest_date",
        ),
        migrations.RemoveField(
            model_name="cultivatedfieldhistory",
            name="pri_crop_yield",
        ),
        migrations.RemoveField(
            model_name="cultivatedfieldhistory",
            name="sec_crop_harvest_date",
        ),
        migrations.RemoveField(
            model_name="cultivatedfieldhistory",
            name="sec_crop_yield",
        ),
        migrations.RemoveField(
            model_name="fieldextensionofficer",
            name="verification_status",
        ),
        migrations.AddField(
            model_name="fieldextensionofficer",
            name="affiliation",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="farmer",
            name="category_type",
            field=models.CharField(
                choices=[("SH", "Smallholder"), ("MLH", "Commercial")],
                default="MLH",
                max_length=3,
            ),
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
                ("created_on", models.DateField(auto_now_add=True)),
                ("updated_on", models.DateField(auto_now=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("receipt_number", models.CharField(max_length=255)),
                ("redemption_date", models.DateField(auto_now=True)),
                ("receipt_identifier", models.CharField(max_length=255, unique=True)),
                ("points_earned", models.IntegerField(default=0, editable=False)),
                (
                    "farmer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="input_purchases",
                        to="farmers.farmer",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="input_purchases",
                        to="vendors.agrovendor",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Harvest",
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
                ("pri_crop_harvest_date", models.DateField(blank=True, null=True)),
                ("sec_crop_harvest_date", models.DateField(blank=True, null=True)),
                ("pri_yield_amount", models.FloatField()),
                ("sec_yield_amount", models.FloatField()),
                ("notes", models.TextField(blank=True)),
                (
                    "field",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="farmers.cultivatedfield",
                    ),
                ),
                (
                    "pri_crop",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pri_harvest",
                        to="farmers.crop",
                    ),
                ),
                (
                    "sec_crop",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="farmers.crop",
                    ),
                ),
            ],
        ),
    ]
