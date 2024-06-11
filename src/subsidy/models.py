from django.db import models

from farmers.models import Farmer


# Create your models here.
class SubsidyProgram(models.Model):

    class Admistrator(models.TextChoices):
        STATE = "M", "State Government"
        NATIONAL = "N", "National Government"
        NGO = "NGO", "Non Governmental Organization"

    title = models.CharField(max_length=255)
    objective = models.CharField(max_length=255, blank=True, null=True)
    source_of_funding = models.CharField(max_length=255, blank=True, null=True)
    program_adminstrator = models.CharField(max_length=255)
    eligibility_criteria = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    number_of_beneficiaries = models.SmallIntegerField(default=0)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    program_adminstrator_type = models.CharField(
        max_length=3, choices=Admistrator.choices
    )
    percentage_of_subsidy = models.DecimalField(
        max_digits=2, decimal_places=2, blank=True, null=True
    )

    administrative_body = models.CharField(
        max_length=255, blank=True, null=True
    )  # body responsible for the subsidy program
    legislation = models.CharField(
        max_length=255, blank=True, null=True
    )  # legislation backing the subsidy program

    def __str__(self):
        return self.title


class FarmerSubsidy(models.Model):
    farmer = models.ForeignKey(
        Farmer, related_name="farmers_subsidy", on_delete=models.CASCADE
    )
    subsidy = models.ForeignKey(
        SubsidyProgram, related_name="farmers_subsidy", on_delete=models.CASCADE
    )
    redemption_date = models.DateField(auto_now_add=True)
    amount_received = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Update the number of beneficiaries in the program
    def update_the_num_of_beneficiaries(self):
        pass
