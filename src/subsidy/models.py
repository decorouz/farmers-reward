from decimal import Decimal

from cities_light.models import Country, Region, SubRegion
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

from core.models import TimeStampedPhoneModel
from farmers.models import Farmer

# Define choices for units
UNIT_CHOICES = [
    ("kg", "kilogram"),
    ("ltr", "liter"),
    ("bag", "bag"),
    ("acre", "Acres"),
    ("ha", "hectare"),
    ("packet", "per packet"),
    ("bottle", "per bottle"),
]


class Fertilizer(TimeStampedPhoneModel):
    class FertilizerChoice(models.TextChoices):
        NPK = "NPK", "Npk"
        UREA = "UREA", "Urea"
        SSP = "SSP", "Single Super Phosphate"
        MP = "MP", "Muriate of Potash"
        DP = "DP", "Diammonium Phosphate"
        OTHER = "OTHER", "Others"

    fertilizer_type = models.CharField(
        max_length=20, choices=FertilizerChoice.choices, null=True, blank=True
    )
    name = models.CharField(max_length=100, unique=True)
    fertilizer_blend = models.CharField(max_length=255, default="20:10:10")
    # current_price = models.DecimalField(
    #     max_digits=7, decimal_places=2, null=True, blank=True
    # )
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="bag")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_fertilizer",
                fields=["name", "fertilizer_type", "fertilizer_blend"],
                condition=Q(
                    name__iexact=Lower("name"),
                ),
            )
        ]

    def __str__(self):
        return f"{self.name}-{self.fertilizer_type}-{self.fertilizer_blend}"


class Seed(TimeStampedPhoneModel):
    class CropChoice(models.TextChoices):
        MAIZE = "MAIZE", "Maize"
        COWPEA = "COWPEA", "Cowpea"
        SOYBEAN = "SOYBEAN", "Soybean"
        RICE = "RICE", "Rice"
        SORGHUM = "SORGHUM", "Sorghum"
        MILLET = "MILLET", "Millet"
        GROUNDNUT = "GROUNDNUT", "Groundnut"
        COTTON = "COTTON", "Cotton"
        SESAME = "SESAME", "Sesame"
        YAM = "YAM", "Yam"
        CASSAVA = "CASSAVA", "Cassava"
        TOMATO = "TOMATO", "Tomatoe"
        PEPPER = "PEPPER", "Pepper"
        OTHER = "OTHER", "Others"

    seed_variety = models.CharField(max_length=255, unique=True, null=True, blank=True)
    gmo = models.BooleanField(default=False)
    # current_price = models.DecimalField(
    #     max_digits=7, decimal_places=2, null=True, blank=True
    # )
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="kg")
    name = models.CharField(
        max_length=20, choices=CropChoice.choices, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    seed_variety__iexact=Lower("seed_variety"),
                ),
                fields=["name", "seed_variety"],
                name="unique_seed",
            )
        ]

    def __str__(self):
        return f"{self.name}-{self.seed_variety}"


class Mechanization(TimeStampedPhoneModel):
    class MechanizationChoice(models.TextChoices):
        PLOUGH = "PLOUGH", "Disc Plough"
        HARROW = "HARROW", "Harrow"
        RIDGE = "RIDGE", "Ridge"
        FERT_APP = "FERT_APP", "Fertilizer Application"
        PLANTING = "PLANTING", "Planting"

    # current_price = models.DecimalField(
    #     max_digits=7, decimal_places=2, null=True, blank=True
    # )

    name = models.CharField(
        max_length=20, choices=MechanizationChoice.choices, null=True, blank=True
    )
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ha")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_mechanization_operation",
            )
        ]

    def __str__(self):
        return f"{self.get_name_display()}"


class Agrochemical(TimeStampedPhoneModel):
    class AgrochemicalChoice(models.TextChoices):
        PRE_EMERGENCE = "PRE", "Pre Emergence Herbicide"
        POST_EMERGENCE = "POS", "Post Emergence Herbicide"
        PESTICIDE = "PES", "Pesticide"
        INSECTICIDE = "INT", "Insecticide"

    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ltr")
    # current_price = models.DecimalField(
    #     max_digits=7, decimal_places=2, null=True, blank=True
    # )
    agrochemical_name = models.CharField(
        max_length=3, choices=AgrochemicalChoice.choices, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    name__iexact=Lower("name"),
                ),
                fields=["agrochemical_name", "name"],
                name="unique_agrochemical_name",
            )
        ]

    def __str__(self):
        return f"{self.name}({self.agrochemical_name})"


# Create your models here.
class SubsidyProgram(models.Model):

    class Sponsor(models.TextChoices):
        STATE = "STATE", "State Government"
        NATIONAL = "NATIONAL", "National Government"
        NGO = "NGO", "Non Governmental Organization"

    title = models.CharField(max_length=255)
    objective = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255)
    sponsor_name = models.CharField(max_length=255, blank=True, null=True)
    program_director = models.CharField(max_length=255, blank=True, null=True)
    legislation = models.CharField(max_length=255, blank=True, null=True)
    number_of_beneficiaries = models.SmallIntegerField(default=0)
    sponsor_type = models.CharField(
        max_length=10,
        choices=Sponsor.choices,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True
    )
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    budget_in_naira = models.DecimalField(
        max_digits=40, decimal_places=2, blank=True, null=True
    )

    def update_active_status(self):
        if self.end_date < timezone.now().date():
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.title}-{self.region}"

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})


class SubsidizedItem(TimeStampedPhoneModel):
    class ItemType(models.TextChoices):
        SEED = "SEED", "Seed"
        FERTILIZER = "FERT", "Fertilizer"
        MECHANIZATION = "MECH", "Mechanization"
        CHEMICAL = "CHEM", "Chemical"

    type = models.CharField(choices=ItemType.choices, max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    subsidized_item = GenericForeignKey("content_type", "object_id")  # content object
    current_price = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id"],
                name="unique_subsidized_item",
            )
        ]

    def get_unit(self):
        if hasattr(self.subsidized_item, "unit"):
            return self.subsidized_item.unit
        return None

    def __str__(self):
        return f"{self.subsidized_item}"


class InputPriceHistory(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item}"


class SubsidyRate(TimeStampedPhoneModel):
    subsidy_program = models.ForeignKey(
        SubsidyProgram, related_name="subsidy_rate", on_delete=models.CASCADE
    )
    subsidized_item = models.ForeignKey(
        SubsidizedItem, related_name="subsidy_rate", on_delete=models.CASCADE
    )
    rate = models.DecimalField(max_digits=4, decimal_places=1, default=Decimal(50.0))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subsidy_program", "subsidized_item"],
                name="unique_subsidy_rate",
            )
        ]

    def __str__(self):
        return f"{self.subsidy_program.region} - {self.subsidized_item}: {self.rate}%"


class SubsidyInstance(TimeStampedPhoneModel):
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    redemption_date = models.DateField(auto_now_add=True)
    # Name of the redemption center.
    # The idea is to make all the major markets a redemption center, likewise the vendors
    redemption_location = models.CharField(max_length=255, null=True, blank=True)
    farmer = models.ForeignKey(
        Farmer, related_name="subsidy_intance", on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        SubsidizedItem,
        related_name="subsidy_intance",
        on_delete=models.PROTECT,
    )
    subsidy_program = models.ForeignKey(
        SubsidyProgram,
        related_name="subsidy_intance",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    discounted_price = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, editable=False,
    )

    @cached_property
    def item_unit(self):
        return self.item.get_unit()

    def save(self, *args, **kwargs):
        # Get the specific subsidy rate for this subsidy program and subsidized item
        try:
            subsidy_rate = SubsidyRate.objects.get(
                subsidy_program=self.subsidy_program,
                subsidized_item=self.item,
            )
            rate = subsidy_rate.rate
        except SubsidyRate.DoesNotExist:
            rate = Decimal(100)  # Default rate if no specific rate is found.
        self.discounted_price = (self.item.current_price) * (1 - rate / 100)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["farmer", "item", "subsidy_program"],
                name="unique_farmer_subsidy",
            )
        ]

    def __str__(self):
        return f"{self.id} - {self.item}"
