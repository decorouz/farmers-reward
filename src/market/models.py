from datetime import date, timedelta

from cities_light.models import Country, Region, SubRegion
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


class PaymentMethod(models.Model):
    class PaymentMethodChoice(models.TextChoices):
        CREDIT_CARD = "CC", "Credit Card"
        MOBILE_MONEY = "MM", "Mobile Money"
        BANK_TRANSFER = "BT", "Bank Transfer"
        POINT_OF_SALE = "POS", "Point of Sale"
        ATM_ON_SITE = "ATM", "ATM on site"
        CASH = "CASH", "Cash"

    type = models.CharField(
        max_length=4,
        choices=PaymentMethodChoice.choices,
        default=PaymentMethodChoice.CASH,
        unique=True,
    )

    def __str__(self) -> str:
        return self.get_type_display()


class Produce(models.Model):
    class UnitChoices(models.IntegerChoices):
        SACK = 1, "100 Kg"
        BASKET = 2, "Basket"
        BAG = 3, "50 Kg"

    class ProduceChoices(models.TextChoices):
        WHEAT = "WHEAT", "Wheat"
        MILLET = "MILLET", "Millet"
        GINGER = "GINGER", "Ginger"
        PADDY_RICE = "PADDY RICE", "Paddy Rice"
        BROWN_COWPEA = "BROWN_COWPEA", "Brown Cowpea"
        WHITE_COWPEA = "WHITE COWPEA", "White Cowpea"
        WHITE_MAIZE = "WHITE MAIZE", "White Maize"
        YELLOW_MAIZE = "YELLOW MAIZE", "Yellow Maize"
        WHITE_SORGHUM = "WHITE SORGHUM", "White Sorghum"
        YELLOW_SORGHUM = "YELLOW_SORGHUM", "Yellow Sorghum"
        SESAME = "SESAME", "Sesame"
        GROUNDNUT = "GROUNDNUT", "Groundnut"
        SOYBEAN = "SOYBEAN", "Soybean"
        IRISH_POTATO = "IRISH POTATO", "Irish Potatoes"
        SWEET_POTATO = "SWEET POTATO", "Sweet Potatoes"
        YAM = "YAM", "Yam"
        CASSAVA = "CASSAVA", "Cassava"
        ONION = "ONION", "Onion"
        OKRA = "OKRA", "Okra"
        TOMATO = "TOMATO", "Fresh Tomato"
        PEPPER = "PEPPER", "Fresh Pepper"
        DRY_TOMATOES = "DRIED TOMATOES", "Dry Tomatoes"
        DRIED_PEPPER = "DRIED PEPPER", "Dry Pepper"
        MILLED_RICE = "MILLED RICE", "Milled Rice"
        GARRI = "GARRI", "Garri"

    name = models.CharField(max_length=50, choices=ProduceChoices.choices, unique=True)
    slug = models.SlugField(unique=True)
    local_name = models.CharField(max_length=50, default="")
    unit = models.IntegerField(choices=UnitChoices.choices, default=UnitChoices.BAG)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "produce"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_name",
            )
        ]

    def __str__(self):
        return self.name  # noqa: F401

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}{self.local_name}")
        self.clean()
        super().save(*args, **kwargs)


class ContactPerson(models.Model):  # replace`BaseModel` with Address
    ROLE = [
        ("MA", "Market Agent"),
        ("ML", "Market Leader"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phonenumber = PhoneNumberField(unique=True)
    role = models.CharField(max_length=255, choices=ROLE, default="MA")
    last_update = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phonenumber", "email"],
                name="unique_contact_person",
            )
        ]

    @admin.display(description="full name")
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Market(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(default="Market Description")
    # image = models.ImageField(upload_to="market_images/", blank=True)
    number_of_vendors = models.IntegerField(default=0)
    operating_hours = models.CharField(max_length=50, default="8:00 AM - 5:00 PM")
    market_frequency = models.SmallIntegerField(
        default=4, validators=[MinValueValidator(1)]
    )
    last_market_day = models.DateField(
        default=date.today,
        verbose_name="Confirmed last market date",
    )
    contact_person = models.OneToOneField(
        ContactPerson,
        on_delete=models.PROTECT,
        related_name="market",
    )

    is_active = models.BooleanField(default=True)
    last_update = models.DateTimeField(auto_now=True)
    payment_methods = models.ManyToManyField(PaymentMethod)
    produce_items = models.ManyToManyField(Produce)
    slug = models.SlugField(unique=True)  # slug

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_market_name",
            )
        ]

    def __str__(self):
        return f"{self.name}-{self.is_market_day}"

    def clean(self):
        super().clean()
        if self.last_market_day and self.last_market_day > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")

    @cached_property
    def next_market_day(self):
        today = date.today()
        days_since_last_market_day = (
            today - self.last_market_day
        ).days % self.market_frequency
        return today + timedelta(
            days=self.market_frequency - days_since_last_market_day
        )

    @property
    def is_market_day(self):
        today = date.today()
        days_since_last_market_day = (today - self.last_market_day).days

        return days_since_last_market_day % self.market_frequency == 0

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})


class MarketDay(models.Model):
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="market_day"
    )
    events = models.TextField(default="Market Event")
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["market", "date"],
                name="unique_market_day",
            )
        ]

    def clean(self):
        # Ensure the date is today
        if not self.market.is_market_day:
            raise ValidationError("MarketDay date must be today.")

    def __str__(self):
        return f"{self.market.name}-{self.date}"


class ProducePrice(models.Model):
    produce = models.ForeignKey(
        Produce, on_delete=models.CASCADE, related_name="produce_price"
    )
    market_day = models.ForeignKey(
        MarketDay, on_delete=models.CASCADE, related_name="produce_price"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["produce", "market_day"],
                name="unique_produce_price",
            )
        ]

    # When we save this what do we want to happen?
    def __str__(self):
        if self.produce:
            return self.produce.name
        return "Deleted Market"


class Address(models.Model):
    street = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    local_govt = models.ForeignKey(
        SubRegion, on_delete=models.CASCADE, related_name="+"
    )
    state = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="+")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="+")
    latitude = models.FloatField(max_length=9, blank=True, null=True)
    longitude = models.FloatField(max_length=9, blank=True, null=True)
    market = models.OneToOneField(Market, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude"],
                name="unique_latitude_longitude",
            ),
        ]
