from django.db import models
from geopy.geocoders import Nominatim

# Each farmer is assigned to an field extension officer


class Address(models.Model):
    display_address = models.CharField(max_length=255, null=True, blank=True)
    local_govt_area = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(max_length=9, blank=True, null=True)
    longitude = models.FloatField(max_length=9, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.longitude and self.latitude:
            geolocator = Nominatim(user_agent="market_app")
            detailed_location = geolocator.reverse(
                (self.latitude, self.longitude), exactly_one=True
            )
            if detailed_location:
                # Reverse geocode to get more detailed address information
                address = detailed_location.raw.get("address", {})
                self.display_address = detailed_location.raw["display_name"]
                self.town = address.get("town", "") or address.get("village", "")
                self.city = address.get("city", "")
                self.local_govt_area = address.get("county", "")
                self.state = address.get("state", "")
                self.country = address.get("country", "")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_latitude_longitude",
            ),
        ]


class ContactPerson(models.Model):
    ROLE = [
        ("extension_agent", "Extension Agent"),
        ("chairman", "Chairman"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PaymentMethod(models.Model):
    class PaymentMethodChoices(models.TextChoices):
        CASH = "CH", "Cash"
        CREDIT_CARD = "CC", "Credit Card"
        POS = "POS", "Point of Sale"
        ATM_ONSITE = "ATM", "ATM Onsite"
        ATM_NEARBY = "ATM_nearby", "ATM within 5 minutes walk"
        BANK_TRANSFER = "BT", "Bank Transfer"

    name = models.CharField(
        max_length=255,
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CASH,
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_name_display()


class Commodity(models.Model):
    CROP_CHOICES = [
        ("wheat", "Wheat"),
        ("corn", "Corn"),
        ("rice", "Rice"),
        ("soybean", "Soybean"),
        ("cotton", "Cotton"),
        ("barley", "Barley"),
        ("oats", "Oats"),
        ("sorghum", "Sorghum"),
        ("millet", "Millet"),
        ("potato", "Potato"),
        ("sugar_beet", "Sugar Beet"),
        ("cassava", "Cassava"),
    ]
    crop_name = models.CharField(max_length=50, choices=CROP_CHOICES)

    class Meta:
        verbose_name_plural = "commodities"
        constraints = [
            models.UniqueConstraint(
                fields=["crop_name"],
                name="unique_crop_name",
            )
        ]

    def __str__(self):
        return self.get_crop_name_display()


class Market(Address):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    number_of_vendors = models.IntegerField(default=0)
    market_day_interval = models.SmallIntegerField(default=4)
    reference_mkt_date = models.DateField(verbose_name="confirmed market date")
    contact_person = models.OneToOneField(
        ContactPerson,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="markets",
    )
    accepted_payment_methods = models.ManyToManyField(
        PaymentMethod,
        blank=True,
        related_name="markets",
    )
    market_products = models.ManyToManyField(
        Commodity, through="MarketCommodityPrice", blank=True, related_name="markets"
    )

    image = models.ImageField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_market_name",
            )
        ]

    def __str__(self):
        return self.name


class MarketCommodityPrice(models.Model):
    market = models.ForeignKey(Market, on_delete=models.PROTECT)
    commodity = models.ForeignKey(Commodity, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "market commodities"
        verbose_name_plural = "market commodities"
        constraints = [
            models.UniqueConstraint(
                fields=["commodity", "market", "date"],
                name="unique_item",
            )
        ]

    def __str__(self):
        return self.market.name
