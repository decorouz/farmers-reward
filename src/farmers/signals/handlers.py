from django.db.models.signals import post_save
from django.dispatch import receiver

from farmers.models import Badge, FarmersMarketTransaction, UserBadge


@receiver(post_save, sender=FarmersMarketTransaction)
def assign_badge(sender, instance, **kwargs):
    farmer = instance.farmer
    total_points = sum(
        transaction.points_earned for transaction in farmer.transactions.all()
    )
    badges = Badge.objects.filter(points_required__lte=total_points)

    for badge in badges:
        UserBadge.objects.create(farmer=farmer, badge=badge)
