from django.db import models


class FarmersMarketTransactionQuerySet(models.QuerySet):

    def get_farmer_total_earned_points_per_year(self, farmer_id, year):
        """Calculate the total points earned by a farmer in a specific year"""
        return (
            self.filter(farmer_id=farmer_id, transaction_date__year=year).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def get_farmer_total_earned_points(self, farmer_id):
        """Calculate the total points earned by a farmer in all markets"""
        return (
            self.filter(farmer_id=farmer_id).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def get_farmer_total_earned_points_per_market(self, farmer_id, market_id):
        """Calculate the total points earned by a farmer in at a specific market"""

        return (
            self.filter(market_id=market_id, farmer_id=farmer_id).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def get_market_total_earned_points(self, market_id):
        """Calculate the total points earned by a market"""
        return (
            self.filter(market_id=market_id).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def get_market_total_earned_points_per_year(self, market_id, year):
        """Calculate the total points earned by a market"""
        return (
            self.filter(market_id=market_id, transaction_date__year=year).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )
