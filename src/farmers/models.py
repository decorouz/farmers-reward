import uuid
from datetime import date

from cities_light.models import Country, Region, SubRegion
from django.contrib import admin
from django.core.validators import MinValueValidator

# from django.contrib.gis.db import models as gis_models
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from market.models import Market, Produce
from market.validators import validate_file_size

from .managers import FarmersMarketTransactionQuerySet


class BaseFarmersModel(models.Model):
    phone_number = PhoneNumberField(max_length=14, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    state = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="+",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="+",
    )
    lga = models.ForeignKey(
        SubRegion,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True


class AgroVendor(BaseFarmersModel):
    name = models.CharField(max_length=100)
    verification_status = models.BooleanField(default=False)
    # When is vendor considered verified?

    def __str__(self) -> str:
        return f"{self.name}-{self.state}-{self.lga}"


class PersonalInfo(BaseFarmersModel):
    class IdentificationType(models.TextChoices):
        NATIONAL_ID = "ND", "National ID"
        PASSPORT = "IP", "International Passport"
        DRIVER_LICENSE = "DL", "Driver's License"

    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    class Education(models.IntegerChoices):
        NONE = 1, "None or did not complete primary school"
        PRIMARY_SCHOOL = 2, "Completed primary school"
        SECONDARY_SCHOOL = 3, "Completed secondary school"
        TIATARY_EDUCATION = 4, "Completed higher education"
        INFORMAL_EDUCARION = 5, "Religious or informal education"
        DONT_KNOW = 888, "Don't know"
        REFUSED = 999, "Refused"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    date_of_birth = models.DateField(
        verbose_name=("Birthday"), default=date(1990, 12, 29)
    )
    state_of_origin = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="+",
    )
    education = models.IntegerField(choices=Education.choices)
    means_of_identification = models.CharField(
        max_length=2,
        choices=IdentificationType.choices,
        default=IdentificationType.NATIONAL_ID,
    )
    identification_number = models.CharField(
        unique=True, max_length=255, blank=True, null=True
    )  # NIN, BVN
    blacklisted = models.BooleanField(default=False)  # Can be appealed
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class FieldExtensionOfficer(PersonalInfo):
    affiliation = models.CharField(
        max_length=255, blank=True, null=True
    )  # School, Training institution, Certificate

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number", "phone_number"],
                name="unique_identification_number",
            ),
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Farmer(PersonalInfo):

    class AgriculturalActivities(models.IntegerChoices):
        CROP_PRODUCER = 1, "Crop Producer"
        LIVESTOCK_PRODUCER = 2, "Livestock Producer"
        BOTH = 3, "Crop and Livestock Producer"

    class CategoryType(models.TextChoices):
        SMALL_HOLDER = "SH", "Smallholder"
        MEDIUM_COMMERCIAL = "MC", "Commercial"

    class FarmsizeCategory(models.TextChoices):
        LESS_THAN_ONE_HA = ("<1", "<1 Hectare")
        ONE_TO_THREE_HA = ("1-3", "1-3 Hectares")
        THREE_TO_FIVE_HA = ("3-5", "3-5 Hectares")
        ABOVE_FIVE_HA = (">5", ">5 Hectares")

    category_type = models.CharField(
        max_length=3,
        choices=CategoryType.choices,
        default=CategoryType.MEDIUM_COMMERCIAL,
    )

    field_extension_officer = models.ForeignKey(
        FieldExtensionOfficer,
        on_delete=models.SET_NULL,
        related_name="farmer",
        null=True,
        blank=True,
    )

    agricultural_activities = models.IntegerField(
        choices=AgriculturalActivities.choices,
        default=AgriculturalActivities.CROP_PRODUCER,
    )
    farmsize = models.CharField(
        max_length=3,
        choices=FarmsizeCategory.choices,
        default=FarmsizeCategory.ONE_TO_THREE_HA,
    )
    has_market_transaction = models.BooleanField(default=False, editable=False)
    has_input_transaction = models.BooleanField(default=False, editable=False)
    is_verified = models.BooleanField(default=False, editable=False)
    earned_points = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, editable=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number", "phone_number"],
                name="farmer_unique_id",
            ),
        ]

    def __str__(self):
        return f"{self.first_name}-{self.last_name}"

    def update_verification_status(self):
        self.is_verified = self.has_market_transaction and self.has_input_transaction
        self.save(update_fields=["is_verified"])

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this farmer"""
        return reverse("farmer_detail", kwargs={"slug": self.slug})


class FarmersMarketTransaction(models.Model):
    """A model to track the transactions between a farmer and a market"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    farmer = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, related_name="mkt_transaction"
    )
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="mkt_transaction"
    )
    produce = models.ForeignKey(Produce, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    transaction_date = models.DateField()
    points_earned = models.IntegerField(
        validators=[MinValueValidator(0)], editable=False
    )
    objects = FarmersMarketTransactionQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["produce", "farmer", "market", "transaction_date"],
                name="unique_mkt_transaction",
            )
        ]

    def clean(self):
        super().clean()
        if self.transaction_date and self.transaction_date != timezone.now().date():
            raise ValidationError("Transaction Data must be curent date")

    def _calculate_earned_points(self):
        """Calculate the points earned by the quantity"""
        return int(self.quantity)

    def save(self, *args, **kwargs):
        self.points_earned = self._calculate_earned_points()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"


class FarmersInputTransaction(models.Model):
    farmer = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, related_name="input_transaction"
    )
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="input_transaction"
    )
    vendor = models.ForeignKey(
        AgroVendor,
        on_delete=models.CASCADE,
        related_name="input_transaction",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=255, unique=True, default="000000")
    receipt_verification_date = models.DateField(default=timezone.now)
    points_earned = models.IntegerField(
        validators=[MinValueValidator(0)], editable=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receipt_number", "farmer"],
                name="unique_receipt_identifier",
            )
        ]

    def clean(self):
        super().clean()
        if not self.market.is_market_day:
            raise ValidationError("Input purchase can only be verified on market days")

    def _calculate_earned_points(self):
        """Calculate the points earned by the purchase amount"""
        return round(int(self.amount / 1000))

    def save(self, *args, **kwargs):
        self.points_earned = self._calculate_earned_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_number}{self.farmer.first_name}{self.receipt_verification_date}"
