import uuid
from datetime import date
from tempfile import mktemp

from cities_light.models import Country, Region, SubRegion
from django.contrib import admin

# from django.contrib.gis.db import models as gis_models
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel
from market.models import Market, Product
from market.validators import validate_file_size
from vendors.models import AgroVendor

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
        Region,
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

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


class FieldExtensionOfficer(PersonalInfo):
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    affiliation = models.CharField(
        max_length=255, blank=True, null=True
    )  # School, Training institution, Certificate

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
        MEDIUM_LARGE_HOLDER = "MLH", "Commercial"

    class FarmsizeCategory(models.TextChoices):
        LESS_THAN_ONE_HA = (
            "<1",
            "<1 Hectare",
        )
        ONE_TO_THREE_HA = (
            "1-3",
            "1-3 Hectares",
        )
        THREE_TO_FIVE_HA = (
            "3-5",
            "3-5 Hectares",
        )
        ABOVE_FIVE_HA = (
            ">5",
            ">5 Hectares",
        )

    category_type = models.CharField(
        max_length=3,
        choices=CategoryType.choices,
        default=CategoryType.MEDIUM_LARGE_HOLDER,
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
    lga = models.ForeignKey(
        SubRegion,
        on_delete=models.SET_NULL,
        related_name="+",
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
    # verification_status = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                name="unique_farmer_id_number",
            )
        ]

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"

    # def update_verification_status(self):
    #     """Two point of farmers verification"""
    #     has_earned_mkt_transaction_pts = FarmersMarketTransaction.objects.filter(
    #         farmer=self
    #     ).exists()
    #     has_input_purchase_pts = FarmersInputTransaction.objects.filter(
    #         farmer=self
    #     ).exists()
    #     if has_earned_mkt_transaction_pts and has_input_purchase_pts:
    #         self.verification_status = True
    #     else:
    #         self.verification_status = False

    #     self.save()
    @admin.display(boolean=True, description="Purchased Input and Sold Produce")
    def confirmed_farmer_status(self):
        has_earned_mkt_transaction_pts = self.transactions.exists()
        has_input_purchase_pts = self.input_purchases.exists()
        return has_earned_mkt_transaction_pts and has_input_purchase_pts

    @admin.display(description="Total Points")
    def total_points(self):
        market_points = (
            self.transactions.aggregate(total=models.Sum("points_earned"))["total"] or 0
        )
        input_points = (
            self.input_purchases.aggregate(total=models.Sum("points_earned"))["total"]
            or 0
        )
        return market_points + input_points

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this farmer"""
        return reverse("farmer_detail", kwargs={"slug": self.slug})


class FarmersMarketTransaction(models.Model):
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["produce", "farmer", "market", "transaction_date"],
                name="unique_mkt_transaction",
                violation_error_message="Transaction already exist",
            )
        ]

    def __str__(self):
        return f"{self.id}"

    def calculate_earned_points(self):
        """Calculate the points earned by the quantity"""
        return int(self.quantity)

    def save(self, *args, **kwargs):
        self.points_earned = self.calculate_earned_points()
        super().save(*args, **kwargs)


class FarmersInputTransaction(TimeStampedModel):
    farmer = models.ForeignKey(
        Farmer, on_delete=models.CASCADE, related_name="input_purchases"
    )
    vendor = models.ForeignKey(
        AgroVendor, on_delete=models.CASCADE, related_name="input_purchases"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=255)
    redemption_date = models.DateField()
    receipt_identifier = models.CharField(max_length=255, editable=False, blank=True)
    points_earned = models.IntegerField(default=0, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["receipt_number", "vendor"],
                name="unique_receipt_identifier",
                violation_error_message="Receipt already exist",
            )
        ]

    def calculate_earned_points(self):
        """Calculate the points earned by the purchase amount"""
        return round(int(self.amount / 1000))

    def save(self, *args, **kwargs):
        # generate a unique identifier for the receipt
        self.receipt_identifier = f"{self.vendor.unique_id}-{self.receipt_number}"
        self.points_earned = self.calculate_earned_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.receipt_identifier}"


class CultivatedField(TimeStampedModel):
    # area = gis_models.PolygonField(null=True, blank=True)
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


# class GeoTag(gis_models.Model):
#     """Geotag farmer by agricultural land"""

#     pass


class Crop(Product):
    variety = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}-{self.variety}"


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


class Harvest(models.Model):
    pri_crop = models.OneToOneField(
        Crop, on_delete=models.CASCADE, related_name="pri_harvest"
    )
    sec_crop = models.OneToOneField(
        Crop,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    field = models.OneToOneField(CultivatedField, on_delete=models.CASCADE)
    pri_crop_harvest_date = models.DateField(null=True, blank=True)
    sec_crop_harvest_date = models.DateField(null=True, blank=True)
    pri_yield_amount = models.FloatField()
    sec_yield_amount = models.FloatField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Harvest for {self.pri_crop}"


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
        MEMBERSHIP_BRONZE = "B", "Bronze"  # KYC complete. 10
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
    """Assign a badge to a farmer upon reaching the required points"""

    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.first_name} earned {self.badge.name}"
