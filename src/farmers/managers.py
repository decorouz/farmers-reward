from django.db import models


class FarmersMarketTransactionQuerySet(models.QuerySet):

    def calculate_annual_points(self, farmer, year):
        """Calculate the points earned by a farmer by year"""
        return (
            self.filter(farmer=farmer, transaction_date__year=year).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def calculate_points_by_market(self, farmer, market):
        """Calculate the total points earned by a farmer in at a specific market"""

        return (
            self.filter(market=market, farmer=farmer).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def calculate_total_points(self, farmer):
        """Calculate the total points earned by a farmer across markets"""
        return (
            self.filter(farmer=farmer).aggregate(total=models.Sum("points_earned"))[
                "total"
            ]
            or 0
        )

    def calculate_market_points_year(self, market, year):
        """Calculate total points accumulated at a market by year"""
        return (
            self.filter(market=market, transaction_date__year=year).aggregate(
                total=models.Sum("points_earned")
            )["total"]
            or 0
        )

    def calculate_market_points(self, market):
        """Calculate the total points earned by a market"""
        return (
            self.filter(market=market).aggregate(total=models.Sum("points_earned"))[
                "total"
            ]
            or 0
        )
