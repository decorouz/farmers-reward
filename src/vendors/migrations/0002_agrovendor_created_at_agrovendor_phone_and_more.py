# Generated by Django 5.1 on 2024-09-01 00:06

import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="agrovendor",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="agrovendor",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=14, null=True, region=None, unique=True
            ),
        ),
        migrations.AddField(
            model_name="agrovendor",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
    ]
