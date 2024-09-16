from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SubsidyInstance


@receiver(post_save, sender=SubsidyInstance)
def update_subsidy_beneficiaries(sender, instance, created, **kwargs):
    """Update the number of beneficiaries in the subsidy program."""
    print(
        SubsidyInstance.objects.filter(
            subsidy_program=instance.subsidy_program, farmer=instance.farmer
        ).exists()
    )
    if (
        created
        and not SubsidyInstance.objects.filter(
            subsidy_program=instance.subsidy_program, farmer=instance.farmer
        ).exists()
    ):
        instance.subsidy_program.current_num_of_beneficiaries += 1
        instance.subsidy_program.save()
