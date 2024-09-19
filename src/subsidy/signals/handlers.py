from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import SubsidyInstance, SubsidyInstanceItem


@receiver(post_save, sender=SubsidyInstance)
def update_subsidy_beneficiaries(sender, instance, created, **kwargs):
    """Update the number of beneficiaries in the subsidy program."""
    if created:
        instance.subsidy_program.current_num_of_beneficiaries += 1
        instance.subsidy_program.save()


# @receiver(post_save, sender=SubsidyInstance)
#     def update_beneficiaries_count(sender, instance, created, **kwargs):
#         if created:
#             subsidy_program = instance.subsidy_program
#             subsidy_program.current_num_of_beneficiaries = subsidy_program.subsidy_instances.count()
#             subsidy_program.save()
