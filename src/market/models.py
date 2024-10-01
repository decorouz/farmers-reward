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

    UNIT_CHOICES = (
        ("BAG", "100 KG"),
        ("50KG", "50 KG"),
        ("100T", "100 Tubers"),
        ("25ltr", "25 liters"),
    )

    class ProduceCategory(models.TextChoices):
        PULSE_NUT = "PN", "Pulse and Nuts"
        CEREAL_TUBER = "CT", "Cereals and Tubers"
        OIL_FAT = "OF", "Oil and Fats"
        MEAT_FISH_EGG = "MFE", "Meat, Fish and Eggs"
        MILK = "MD", "Milk and Dairy"
        VEGETABLE = "VF", "Vegetable and Fruits"
        NON_FOOD = "NF", "Non Food"
        MISCELLANEOUS = "MS", "Miscellaneous Food"

    name = models.CharField(max_length=50, unique=True)
    extra = models.CharField(
        max_length=50, default="", help_text="eg. brown beans, shelled groudnut"
    )
    local_name = models.CharField(max_length=50, default="")
    category = models.CharField(
        max_length=3,
        choices=ProduceCategory.choices,
        default=ProduceCategory.CEREAL_TUBER,
    )
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, default="BAG")
    last_update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "commodities"
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_commodity_name",
            )
        ]

    def __str__(self):
        return self.name_detail  # noqa: F401

    @property
    def name_detail(self):
        return f"{self.name}({self.extra})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.extra}-{self.local_name}")
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

    @property
    def name_location(self):
        return

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
    date = models.DateField(default=date.today)

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
        return f"{self.date}"


class ProducePrice(models.Model):

    class PriceType(models.TextChoices):
        WHOLESALE = "W", "Wholesale"
        RETAIL = "R", "Retail"

    produce = models.ForeignKey(
        Produce, on_delete=models.CASCADE, related_name="produce_price"
    )
    market_day = models.ForeignKey(
        MarketDay, on_delete=models.CASCADE, related_name="produce_price"
    )
    price_type = models.CharField(
        max_length=1,
        choices=PriceType.choices,
        default=PriceType.WHOLESALE,
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
