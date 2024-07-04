import uuid
from datetime import date

from cities_light.models import Country, Region, SubRegion
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel
from market.models import Market, Product
from market.validators import validate_file_size

from .managers import FarmersMarketTransactionQuerySet


class FarmersCooperative(TimeStampedModel):
    name = models.CharField(max_length=255)
    chairman = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, unique=True)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    registeration_date = models.DateField(auto_now_add=True)
    registration_number = models.CharField(max_length=255, unique=True)
    verification_status = models.BooleanField(default=False)
    number_of_members = models.SmallIntegerField(default=0)
    blacklisted = models.BooleanField(default=False)  # Can be appealed

    def __str__(self):
        return self.name


class PersonalInfo(TimeStampedModel):
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
    date_of_birth = models.DateField(verbose_name=("Birthday"), null=True, blank=True)
    state_of_origin = models.ForeignKey(
        SubRegion,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    state_of_residence = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )
    education = models.IntegerField(choices=Education.choices)
    phone_number = models.CharField(max_length=13, unique=True, default="9****")
    verification_status = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    blacklisted = models.BooleanField(default=False)  # Can be appealed
    means_of_identification = models.CharField(
        max_length=2,
        choices=IdentificationType.choices,
        default=IdentificationType.NATIONAL_ID,
    )
    identification_number = models.CharField(
        unique=True, max_length=255, blank=True, null=True
    )  # NIN, BVN
    id_photo = models.FileField(
        upload_to="farmers/identification_proof/",
        validators=[validate_file_size],
        blank=True,
        null=True,
    )
    captured_photo = models.ImageField(
        upload_to="farmers/captured_photo/",
        validators=[validate_file_size],
        blank=True,
        null=True,
    )
    verification_date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number", "phone_number"],
                name="unique_identification_number",
            ),
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name

    # Update verification status upon verification of NIN
    def update_verification_status(self):
        """Upon verification of NIN and ID proof,
        update the verification status"""
        pass

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class FieldExtensionOfficer(PersonalInfo):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                name="unique_feo_id_number",
            )
        ]

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse("fieldextensionofficer_details", kwargs={"slug": self.slug})


class Farmer(PersonalInfo):

    class AgriculturalActivities(models.IntegerChoices):
        CROP_PRODUCER = 1, "Crop Producer"
        LIVESTOCK_PRODUCER = 2, "Livestock Producer"
        BOTH = 3, "Crop and Livestock Producer"

    class CategoryType(models.TextChoices):
        SMALL_HOLDER = "SH", "Smallholder"
        SMALL_MEDIUM_HOLDER = "SMH", "Small to Medium Holder"

    category_type = models.CharField(
        max_length=3,
        choices=CategoryType.choices,
        default=CategoryType.SMALL_MEDIUM_HOLDER,
    )
    cooperative_society = models.ForeignKey(
        FarmersCooperative,
        on_delete=models.PROTECT,
        related_name="farmer",
        null=True,
        blank=True,
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
    farmsize = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                name="unique_farmer_id_number",
            )
        ]

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"

    # Generate a unique identification number for the farmer
    def generate_farmer_id(self):
        """Upon registration, generate a unique
        identification number for the farmer"""
        pass

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this farmer"""
        return reverse("farmer_detail", kwargs={"slug": self.slug})


class FarmersMarketTransaction(TimeStampedModel):
    """A model to track the transactions between a farmer and a market"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    farmer = models.ForeignKey(
        Farmer, on_delete=models.RESTRICT, related_name="transactions"
    )
    market = models.ForeignKey(
        Market, on_delete=models.RESTRICT, related_name="transactions"
    )
    produce = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    transaction_date = models.DateField(auto_now=True)
    points_earned = models.IntegerField(default=0, editable=False)
    objects = FarmersMarketTransactionQuerySet.as_manager()

    def __str__(self):
        return f"{self.id}--{self.market.id}--{self.farmer.id}"

    def save(self, *args, **kwargs):
        self.points_earned = self.calculate_earned_points()
        super().save(*args, **kwargs)

    def calculate_earned_points(self):
        """Calculate the points earned by the quantity"""
        return int(self.quantity)


class CultivatedField(TimeStampedModel):
    field_size = models.FloatField(null=True, blank=True)
    soil_test = models.BooleanField(default=False)
    town = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    sub_region = models.ForeignKey(
        SubRegion, on_delete=models.PROTECT, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True
    )

    latitude = models.FloatField(null=True, blank=True)
    logitude = models.FloatField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id"],
                name="unique_field_name",
            )
        ]

    def __str__(self):
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse("cultivatedfield_detail", kwargs={"slug": self.slug})


class CultivatedFieldHistory(TimeStampedModel):
    """Keep track of the history of a cultivated field"""

    class FarmingPractice(models.TextChoices):
        MONO_CROPPING = "MONO", "Mono Cropping"
        MULTI_CROPPING = "MULTI", "Multi Cropping"
        INTER_CROPPING = "INTER", "Inter-Cropping"

    cultivated_field = models.ForeignKey(
        CultivatedField,
        on_delete=models.CASCADE,
        related_name="cultivated_field_history",
        null=True,
        blank=True,
    )
    farming_system = models.CharField(
        max_length=7,
        choices=FarmingPractice.choices,
        default=FarmingPractice.MONO_CROPPING,
    )
    farmer = models.ForeignKey(
        Farmer, on_delete=models.SET_NULL, related_name="cultivated_fields", null=True
    )
    primary_crop_type = models.CharField(max_length=50, default="Wheat")
    secondary_crop_type = models.CharField(max_length=50, null=True, blank=True)
    pri_crop_planting_date = models.DateField(null=True, blank=True)
    sec_crop_planting_date = models.DateField(null=True, blank=True)
    pri_crop_harvest_date = models.DateField(null=True, blank=True)
    sec_crop_harvest_date = models.DateField(null=True, blank=True)
    pri_crop_yield = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sec_crop_yield = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    fertilizer_use = models.BooleanField(default=False)
    fertilizer_qty = models.FloatField(null=True, blank=True)
    manure_compost_use = models.BooleanField(default=False)
    average_ridge_weed_biomass = models.FloatField(null=True, blank=True)
    striga = models.BooleanField(default=False)
    row_spacing = models.FloatField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cultivated_field", "created_on"],
                name="unique_cultivated_field_history",
            )
        ]

    def __str__(self):
        return f"{self.cultivated_field} {self.year}"

    @property
    def year(self):
        return self.created_on.year

    def calculate_fertilizer_rate(self):
        pass


class SoilProperty(models.Model):
    cultivated_field = models.ForeignKey(
        CultivatedField, on_delete=models.CASCADE, related_name="soil_properties"
    )
    texture = models.CharField(max_length=100)
    pH = models.DecimalField(max_digits=4, decimal_places=2)
    organic_matter = models.DecimalField(max_digits=5, decimal_places=2)
    nitrogen_content = models.DecimalField(max_digits=5, decimal_places=2)
    phosphorus_content = models.DecimalField(max_digits=5, decimal_places=2)
    potassium_content = models.DecimalField(max_digits=5, decimal_places=2)
    soil_test_date = models.DateField(auto_now=True)
    soil_lab = models.CharField(max_length=255, default="IITA Soil Lab")
    test_results_file = models.FileField(
        upload_to="soil_tests/",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cultivated_field", "soil_test_date"],
                name="unique_soil_test_date",
            )
        ]

    def __str__(self):
        return f"{self.cultivated_field} {self.soil_test_date}"


class Badge(TimeStampedModel):
    class BadgeType(models.TextChoices):
        MEMBERSHIP_BRONZE = "B", "Bronze"
        MEMBERSHIP_SILVER = "S", "Silver"
        MEMBERSHIP_GOLD = "G", "Gold"

    name = models.CharField(
        max_length=255, choices=BadgeType.choices, default=BadgeType.MEMBERSHIP_BRONZE
    )
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="farmers/badges/")
    image_thumbnail = models.ImageField(
        upload_to="badges/thumbnails/", blank=True, null=True
    )
    points_required = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


# UserBadge Model
class UserBadge(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.first_name} earned {self.badge.name}"
