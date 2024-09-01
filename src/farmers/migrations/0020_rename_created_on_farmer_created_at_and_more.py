# Generated by Django 5.1 on 2024-09-01 00:06

import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0019_alter_farmer_phone_alter_farmerscooperative_phone_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="farmer",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="farmer",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="farmerscooperative",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="farmerscooperative",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="fieldextensionofficer",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="fieldextensionofficer",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.AddField(
            model_name="badge",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="badge",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="cultivatedfield",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="cultivatedfield",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="cultivatedfieldhistory",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="cultivatedfieldhistory",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="farmersinputtransaction",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmersinputtransaction",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="farmersmarkettransaction",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="farmersmarkettransaction",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="harvest",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="harvest",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="soilproperty",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="soilproperty",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="userbadge",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userbadge",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="farmer",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=14, null=True, region=None, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="farmerscooperative",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=14, null=True, region=None, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="fieldextensionofficer",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=14, null=True, region=None, unique=True
            ),
        ),
    ]
