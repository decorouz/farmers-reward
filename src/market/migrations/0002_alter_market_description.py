# Generated by Django 5.1.1 on 2024-09-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="market",
            name="description",
            field=models.TextField(default="Market Description"),
        ),
    ]
