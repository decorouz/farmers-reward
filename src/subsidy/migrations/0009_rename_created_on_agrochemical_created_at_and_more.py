# Generated by Django 5.1 on 2024-09-01 00:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subsidy", "0008_rename_created_on_inputpricehistory_created_at_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="agrochemical",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="agrochemical",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="fertilizer",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="fertilizer",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="mechanization",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="mechanization",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="seed",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="seed",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="subsidizeditem",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subsidizeditem",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="subsidyinstance",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subsidyinstance",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="subsidyrate",
            old_name="created_on",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subsidyrate",
            old_name="updated_on",
            new_name="updated_at",
        ),
        migrations.RemoveField(
            model_name="agrochemical",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="fertilizer",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="mechanization",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="seed",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="subsidizeditem",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="subsidyinstance",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="subsidyrate",
            name="phone",
        ),
        migrations.AddField(
            model_name="inputpricehistory",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name="subsidyprogram",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subsidyprogram",
            name="updated_at",
            field=models.DateField(auto_now=True),
        ),
    ]
