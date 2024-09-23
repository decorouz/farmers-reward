# Generated by Django 5.1.1 on 2024-09-22 04:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0004_remove_market_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="marketday",
            name="market",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="market_day",
                to="market.market",
            ),
        ),
    ]
