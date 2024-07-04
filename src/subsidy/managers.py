from django.db import models


class SubsidyInstanceQuerySet(models.QuerySet):
    def get_total_subsidy_disbursed(self, subsidy_program_id):
        """Calculate the total subsidy disbursed for a subsidy program"""
        return (
            self.filter(subsidy_program_id=subsidy_program_id).aggregate(
                total=models.Sum("discounted_price")
            )["total"]
            or 0
        )

    def get_total_subsidy_redeemed_per_farmer(self, farmer_id, subsidy_program_id):
        """Calculate the total subsidy redeemed by a farmer per program"""
        return (
            self.filter(
                farmer_id=farmer_id, subsidy_program_id=subsidy_program_id
            ).aggregate(total_per_prog=models.Sum("discounted_price"))["total_per_prog"]
            or 0
        )

    def get_total_subsidy_received_per_farmer(self, farmer_id):
        return (
            self.filter(farmer_id=farmer_id).aggregate(
                total_per_farmer=models.Sum("discounted_price")
            )["total_per_farmer"]
            or 0
        )


class InputPriceHistoryQuerySet(models.QuerySet):

    def get_latest_price(self, item_id):
        return self.filter(item_id=item_id).order_by("-created_on").first()

    def get_average_price_of_item_per_year(self, item_id, year):
        return (
            self.filter(item_id=item_id, created_on__year=year).aggregate(
                avg_price=models.Avg("price")
            )["avg_price"]
            or 0
        )
