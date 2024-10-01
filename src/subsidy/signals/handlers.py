from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SubsidyDisbursement


@receiver(post_save, sender=SubsidyDisbursement)
def update_subsidy_beneficiaries(sender, instance, created, **kwargs):
    """Update the number of beneficiaries in the subsidy program."""
    if created:
        instance.subsidy_program.current_num_of_beneficiaries += 1
        instance.subsidy_program.save()
