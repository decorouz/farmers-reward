from datetime import datetime

from django.db import models

from market.models import Commodity, Market


class PersonalInfo(models.Model):
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
    education = models.IntegerField(choices=Education.choices)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    verification_status = models.BooleanField(default=False)

    means_of_identification = models.CharField(
        max_length=2,
        choices=IdentificationType.choices,
        default=IdentificationType.NATIONAL_ID,
    )
    identification_number = models.CharField(
        max_length=255, blank=True, null=True
    )  # NIN, BVN
    id_photo = models.FileField(
        upload_to="identification_proof/", blank=True, null=True
    )
    captured_photo = models.ImageField(
        upload_to="captured_photo/", blank=True, null=True
    )
    registration_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    # Update verification status upon verification of NIN
    def update_verification_status(self):
        """Upon verification of NIN and ID proof,
        update the verification status"""
        pass

    def __str__(self):
        return self.first_name + " " + self.last_name


class FarmersCooperative(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    registeration_date = models.DateField(auto_now_add=True)
    registration_number = models.CharField(max_length=255)
    verification_status = models.BooleanField(default=False)
    number_of_members = models.SmallIntegerField(default=0)
    blacklisted = models.BooleanField(default=False)  # Can be appealed

    def __str__(self):
        return self.name


class FieldExtensionOfficer(PersonalInfo):
    email = models.EmailField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                name="unique_feo_id_number",
            )
        ]


class FarmersAccountDetail(models.Model):
    bank_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255)


class Farmer(PersonalInfo):

    class AgriculturalActivities(models.IntegerChoices):
        CROP_PRODUCER = 1, "Crop Producer"
        LIVESTOCK_PRODUCER = 2, "Livestock Producer"
        BOTH = 3, "Crop and Livestock Producer"

    class CategoryType(models.TextChoices):
        SMALL_HOLDER = "SH", "Smallholder"
        SMALL_MEDIUM_HOLDER = "SMH", "Small to Medium Holder"

    farmsize = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.PositiveSmallIntegerField(default=0)
    blacklisted = models.BooleanField(default=False)  # Can be appealed
    updated_at = models.DateTimeField(auto_now=True)
    category_type = models.CharField(
        max_length=3,
        choices=CategoryType.choices,
        default=CategoryType.SMALL_MEDIUM_HOLDER,
    )
    cooperative_society = models.ForeignKey(
        FarmersCooperative,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    account_number = models.OneToOneField(
        FarmersAccountDetail,
        on_delete=models.DO_NOTHING,
        related_name="farmer",
        null=True,
        blank=True,
    )
    field_extension_officer = models.ForeignKey(
        FieldExtensionOfficer,
        on_delete=models.PROTECT,
        related_name="farmer",
        null=True,
        blank=True,
    )

    agricultural_activities = models.IntegerField(
        choices=AgriculturalActivities.choices,
        default=AgriculturalActivities.CROP_PRODUCER,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_number"],
                name="unique_farmer_id_number",
            )
        ]

    # Generate a unique identification number for the farmer
    def generate_farmer_id(self):
        """Upon registration, generate a unique
        identification number for the farmer"""
        pass


class FarmersMarketTransaction(models.Model):
    # Basket of Vegetables
    # Bag of grains
    # Tubers
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT)
    market = models.ForeignKey(Market, on_delete=models.PROTECT)
    produce = models.ForeignKey(Commodity, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    transaction_date = models.DateField(auto_now_add=True)
    points_earned = models.PositiveSmallIntegerField()

    def calculate_point_earned(self):
        """Calculate the points earned by the quantity"""
        pass


class CultivatedField(models.Model):
    class FarmingPractice(models.IntegerChoices):
        MONO_CROPPING = 1, "Mono Cropping"
        MULTI_CROPPING = 2, "Multi Cropping"
        MIXED_CROPPING = 3, "Mixed Cropping"

    field_name = models.CharField(max_length=255, blank=True, null=True)
    farmer = models.ForeignKey(
        Farmer, on_delete=models.PROTECT, related_name="cultivated_fields"
    )
    cropping_system = models.IntegerField(
        choices=FarmingPractice.choices, default=FarmingPractice.MONO_CROPPING
    )
    field_size = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    crop = models.ForeignKey(
        Commodity,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    crop_yield = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    crop_planting_date = models.DateField(null=True, blank=True)
    crop_harvest_date = models.DateField(null=True, blank=True)
    crop_harvest_yield = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    town = models.CharField(max_length=255)
    local_govt_area = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    date_captured = models.DateField(auto_now_add=True)
    soil_test_date = models.DateField(null=True, blank=True)
    test_results_file = models.FileField(
        upload_to="soil_tests/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.field_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.field_name:
            self.field_name = f"{self.state}/{self.local_govt_area}/{self.town}/{self.date_captured.year}/{self.id}"
            super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["field_name"],
                name="unique_field_name",
            )
        ]
