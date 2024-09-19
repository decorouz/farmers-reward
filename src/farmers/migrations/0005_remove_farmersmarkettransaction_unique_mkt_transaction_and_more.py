# Generated by Django 5.1.1 on 2024-09-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "farmers",
            "0004_remove_farmersinputtransaction_unique_receipt_identifier_and_more",
        ),
        ("market", "0005_alter_marketday_mkt_date"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="farmersmarkettransaction",
            name="unique_mkt_transaction",
        ),
        migrations.AddConstraint(
            model_name="farmersmarkettransaction",
            constraint=models.UniqueConstraint(
                fields=("produce", "farmer", "market", "transaction_date"),
                name="unique_mkt_transaction",
            ),
        ),
    ]
