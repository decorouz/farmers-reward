# Generated by Django 5.1.1 on 2024-09-19 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "farmers",
            "0014_remove_farmersinputtransaction_unique_receipt_identifier_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="farmer",
            name="verification_date",
        ),
        migrations.RemoveField(
            model_name="fieldextensionofficer",
            name="verification_date",
        ),
        migrations.AlterField(
            model_name="farmersinputtransaction",
            name="vendor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="input_purchases",
                to="farmers.agrovendor",
            ),
        ),
    ]
