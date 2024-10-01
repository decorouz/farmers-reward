from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Farmer, FarmersInputTransaction, FarmersMarketTransaction


@receiver(post_save, sender=FarmersMarketTransaction)
def update_farmer_market_transaction_status(sender, instance, created, **kwargs):
    if created:
        Farmer.objects.filter(
            pk=instance.farmer.pk, has_market_transaction=False
        ).update(
            has_market_transaction=True,
            is_verified=models.Case(
                models.When(has_input_transaction=True, then=True), default=False
            ),
        )


@receiver(post_save, sender=FarmersInputTransaction)
def update_farmer_input_transaction_status(sender, instance, created, **kwargs):
    if created and instance.receipt_verification_date:
        Farmer.objects.filter(
            pk=instance.farmer.pk, has_input_transaction=False
        ).update(
            has_input_transaction=True,
            is_verified=models.Case(
                models.When(has_market_transaction=True, then=True), default=False
            ),
        )


@receiver(post_delete, sender=FarmersInputTransaction)
def update_farmer_has_input_transactions(sender, instance, **kwarg):
    farmer = instance.farmer
    has_input_transaction = FarmersInputTransaction.objects.filter(
        farmer=farmer
    ).exists()
    if not has_input_transaction:
        print("\n Did we ge here")
        farmer.has_input_transaction = False
        farmer.is_verified = False
        farmer.save(update_fields=["has_input_transaction", "is_verified"])

    # @admin.display(description="Total Points")
    # def total_points(self):
    #     market_points = (
    #         self.transactions.aggregate(total=models.Sum("points_earned"))["total"] or 0
    #     )
    #     input_points = (
    #         self.input_purchases.aggregate(total=models.Sum("points_earned"))["total"]
    #         or 0
    #     )
    #     return market_points + input_points
