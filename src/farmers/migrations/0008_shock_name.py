# Generated by Django 5.0.6 on 2024-06-28 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0007_alter_cultivatedcrop_crop"),
    ]

    operations = [
        migrations.AddField(
            model_name="shock",
            name="name",
            field=models.CharField(default="Flooding", max_length=255),
        ),
    ]
