from django.db import models
from geopy.geocoders import Nominatim


class ContactPerson(models.Model):
    ROLE = [
        ("extension_agent", "Extension Agent"),
        ("chairman", "Chairman"),
    ]
    name = models.CharField(max_length=100)
    cell_phone_number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=100, choices=ROLE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Market(models.Model):
    class PaymentMethodChoices(models.TextChoices):
        CASH = "CH", "Cash"
        CREDIT_CARD = "CC", "Credit Card"
        POS = "POS", "Point of Sale"
        ATM_ONSITE = "ATM", "ATM Onsite"
        ATM_NEARBY = "ATM_nearby", "ATM within 5 minutes walk"
        BANK_TRANSFER = "BT", "Bank Transfer"

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    number_of_vendors = models.IntegerField(default=0)
    market_day_interval = models.SmallIntegerField(default=4)
    reference_mkt_date = models.DateField(verbose_name="confirmed market date")
    contact_person = models.OneToOneField(
        "ContactPerson",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="market",
    )
    accepted_payment_method = models.CharField(
        choices=PaymentMethodChoices.choices,
        max_length=100,
        default=PaymentMethodChoices.CASH,
    )
    market_products = models.ManyToManyField(
        "Commodity", through="MarketCommodityPrice", blank=True, related_name="markets"
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    local_govt_area = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(max_length=9, blank=True, null=True)
    longitude = models.FloatField(max_length=9, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            geolocator = Nominatim(user_agent="your_app_name")
            location = geolocator.geocode(self.address)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
                # Reverse geocode to get more detailed address information
                detailed_location = geolocator.reverse(
                    (location.latitude, location.longitude),
                    exactly_one=True,
                )
                address = detailed_location.raw.get("address", {})
                self.town = address.get("village", "")
                self.city = address.get("city", "")
                self.local_govt_area = address.get("county", "")
                self.state = address.get("state", "")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_market_name",
            ),
            models.UniqueConstraint(
                fields=["longitude", "latitude"],
                name="unique_market_location",
            ),
        ]

    def __str__(self):
        return self.name


class MarketCommodityPrice(models.Model):
    market = models.ForeignKey("Market", on_delete=models.DO_NOTHING)
    commodity = models.ForeignKey("Commodity", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        unique_together = ("market", "commodity", "date")


class Commodity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Commodities"

    def __str__(self):
        return self.name
