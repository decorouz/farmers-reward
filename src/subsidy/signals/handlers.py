from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from subsidy.models import (  # Agrochemical,; Fertilizer,; Mechanization,; Seed,
    InputPriceHistory,
    SubsidizedItem,
    SubsidyInstance,
)


# @receiver(pre_save, sender=Fertilizer)
# @receiver(pre_save, sender=Agrochemical)
# @receiver(pre_save, sender=Mechanization)
# @receiver(pre_save, sender=Seed)
@receiver(pre_save, sender=SubsidizedItem)
def update_input_price_history(sender, instance, *args, **kwargs):
    """Create a record of price changes in the input price history table."""

    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.current_price != instance.current_price:
            InputPriceHistory.objects.create(
                content_type=ContentType.objects.get_for_model(sender),
                object_id=instance.pk,
                price=instance.current_price,
                unit=instance.unit,
            )


@receiver(post_save, sender=SubsidyInstance)
def update_subsidy_beneficiaries(sender, instance, *args, **kwargs):
    """Update the number of beneficiaries in the subsidy program."""
    if (
        kwargs["created"]
        and not SubsidyInstance.objects.filter(
            subsidy_program=instance.subsidy_program, farmer=instance.farmer
        ).exists()
    ):
        instance.subsidy_program.number_of_beneficiaries += 1
        instance.subsidy_program.save()
