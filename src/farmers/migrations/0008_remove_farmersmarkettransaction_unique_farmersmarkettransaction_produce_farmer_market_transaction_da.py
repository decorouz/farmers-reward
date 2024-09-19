# Generated by Django 5.1.1 on 2024-09-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "farmers",
            "0007_remove_farmersmarkettransaction_unique_farmersmarkettransaction_produce_farmer_market_transaction_da",
        ),
        ("market", "0005_alter_marketday_mkt_date"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="farmersmarkettransaction",
            name="unique_farmersmarkettransaction_produce_farmer_market_transaction_date",
        ),
        migrations.AddConstraint(
            model_name="farmersmarkettransaction",
            constraint=models.UniqueConstraint(
                fields=("produce", "farmer"),
                name="unique_farmersmarkettransaction_produce_farmer_market_transaction_date",
            ),
        ),
    ]
