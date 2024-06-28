from cities_light.models import Country, Region, SubRegion
from django.db import models
from django.urls import reverse
from geopy.geocoders import Nominatim

from core.models import TimeStampedModel

from .validators import validate_file_size

# Each farmer is assigned to an field extension officer


class Address(TimeStampedModel):
    display_address = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    sub_region = models.ForeignKey(
        SubRegion, on_delete=models.SET_NULL, null=True, blank=True
    )
    # city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
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
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_latitude_longitude",
            ),
        ]


class ContactPerson(TimeStampedModel):
    ROLE = [
        ("extension_agent", "Extension Agent"),
        ("chairman", "Chairman"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLE, default="extension_agent")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone", "email"],
                name="unique_contact_person",
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PaymentMethod(TimeStampedModel):
    class PaymentMethodChoices(models.IntegerChoices):
        CASH = 1, "Cash"
        CREDIT_CARD = 2, "Credit Card"
        POS = 3, "Point of Sale"
        ATM_ONSITE = 4, "ATM Onsite"
        ATM_NEARBY = 5, "ATM within 5 minutes walk"
        BANK_TRANSFER = 6, "Bank Transfer"

    name = models.IntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.CASH,
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_name_display()


class Product(TimeStampedModel):
    class UnitChoices(models.IntegerChoices):
        KG = 1, "100 Kg Sack"
        BASKET = 2, "50 Kg Basket"
        SACK = 3, "50 Kg Sack"
        BAG = 4, "25 Kg Sack"

    class ProductChoices(models.TextChoices):
        WHEAT = "WHEAT", "Wheat"
        MILLED_RICE = "MILLED RICE", "Milled Rice"
        PADDY_RICE = "PADDY RICE", "Paddy Rice"
        BROWN_COWPEA = "BROWN_COWPEA", "Brown Cowpea"
        WHITE_COWPEA = "WHITE COWPEA", "White Cowpea"
        WHITE_MAIZE = "WHITE MAIZE", "White Maize"
        YELLOW_MAIZE = "YELLOW MAIZE", "Yellow Maize"
        SOYBEAN = "SOYBEAN", "Soybean"
        WHITE_SORGHUM = "WHITE SORGHUM", "White Sorghum"
        YELLOW_SORGHUM = "YELLOW_SORGHUM", "Yellow Sorghum"
        SWEET_POTATOES = "SWEET POTATOES", "Sweet Potatoes"
        IRISH_POTATOES = "IRISH POTATOES", "Irish Potatoes"
        ONION = "ONION", "Onion"
        TOMATO = "TOMATO", "Tomato"
        DRY_TOMATOES = "DRIED TOMATOES", "Dry Tomatoes"
        PEPPER = "PEPPER", "Pepper"

    name = models.CharField(max_length=50, choices=ProductChoices.choices)
    slug = models.SlugField(unique=True)
    local_name = models.CharField(max_length=50, blank=True, null=True)
    unit = models.IntegerField(
        choices=UnitChoices.choices, default=UnitChoices.KG, blank=True
    )

    class Meta:
        verbose_name_plural = "products"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "name",
                    "local_name",
                ],
                name="unique_name",
            )
        ]

    def __str__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})


# Only admin can create a market
class Market(Address):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # slug
    description = models.TextField(blank=True, null=True)
    number_of_vendors = models.IntegerField(default=0)
    operating_hours = models.CharField(max_length=50, default="8:00 AM - 5:00 PM")
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
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_market_name",
            )
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})


class MarketProduct(TimeStampedModel):
    market = models.ForeignKey(
        Market, on_delete=models.SET_NULL, related_name="market_product", null=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="market_product"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mkt_date = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "market", "mkt_date"],
                name="unique_item",
            )
        ]

    # When we save this what do we want to happen?
    def __str__(self):
        if self.market:
            return self.market.name
        return "Deleted Market"


class MarketImage(TimeStampedModel):
    """One market can have many images"""

    market = models.ForeignKey(
        Market,
        on_delete=models.PROTECT,
        related_name="market_images",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="market/images/%Y/%m/%d/",
        validators=[validate_file_size],
        blank=True,
        null=True,
    )
