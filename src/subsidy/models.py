from decimal import Decimal

from cities_light.models import Country, Region, SubRegion
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.forms import ValidationError
from django.utils import timezone
from django.utils.functional import cached_property

from core.models import TimeStampModel
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


class Fertilizer(TimeStampModel):
    class FertilizerChoice(models.TextChoices):
        NPK = "NPK", "Npk"
        UREA = "UREA", "Urea"
        SSP = "SSP", "Single Super Phosphate"
        MP = "MP", "Muriate of Potash"
        DP = "DP", "Diammonium Phosphate"
        OTHER = "OTHER", "Others"

    brand = models.CharField(max_length=100, unique=True)
    fertilizer_type = models.CharField(
        max_length=20, choices=FertilizerChoice.choices, null=True, blank=True
    )
    fertilizer_blend = models.CharField(max_length=255, default="20:10:10")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_fertilizer",
                fields=["brand", "fertilizer_type", "fertilizer_blend"],
                condition=Q(
                    brand__iexact=Lower("brand"),
                ),
            )
        ]

    def __str__(self):
        return f"{self.brand}-{self.fertilizer_type}-{self.fertilizer_blend}"


class Seed(TimeStampModel):
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

    brand = models.CharField(max_length=100, default="Seedco")
    name = models.CharField(
        max_length=20, choices=CropChoice.choices, null=True, blank=True
    )
    seed_variety = models.CharField(max_length=255, unique=True, null=True, blank=True)

    gmo = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    seed_variety__iexact=Lower("seed_variety"),
                ),
                fields=["brand", "name", "seed_variety"],
                name="unique_seed",
            )
        ]

    def __str__(self):
        return f"{self.brand}-{self.seed_variety}"


class Mechanization(TimeStampModel):
    class MechanizationChoice(models.TextChoices):
        PLOUGH = "PLOUGH", "Disc Plough"
        HARROW = "HARROW", "Harrow"
        RIDGE = "RIDGE", "Ridge"
        FERT_APP = "FERT_APP", "Fertilizer Application"
        PLANTING = "PLANTING", "Planting"

    operation = models.CharField(
        max_length=20, choices=MechanizationChoice.choices, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["operation"],
                name="unique_mechanization_operation",
            )
        ]

    def __str__(self):
        return f"{self.get_name_display()}"  # type: ignore


class Agrochemical(TimeStampModel):
    class AgrochemicalChoice(models.TextChoices):
        PRE_EMERGENCE = "PRE", "Pre Emergence Herbicide"
        POST_EMERGENCE = "POS", "Post Emergence Herbicide"
        PESTICIDE = "PES", "Pesticide"
        INSECTICIDE = "INT", "Insecticide"

    brand = models.CharField(max_length=255, unique=True, null=True, blank=True)
    type = models.CharField(
        max_length=3, choices=AgrochemicalChoice.choices, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    brand__iexact=Lower("brand"),
                ),
                fields=["brand", "type"],
                name="unique_agrochemical_brand",
            )
        ]

    def __str__(self):
        return f"{self.brand}({self.type})"


class SubsidyProgram(TimeStampModel):
    class ProgramLevel(models.TextChoices):
        STATE = "STATE", "State"
        NATIONAL = "NATIONAL", "National"

    title = models.CharField(max_length=255)
    implementation_details = models.TextField(null=True, blank=True)
    sponsor_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(
        max_length=10, choices=ProgramLevel.choices, default=ProgramLevel.NATIONAL
    )
    target_num_of_beneficiaries = models.SmallIntegerField(default=200)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, null=True, blank=True
    )
    state = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    budget_in_naira = models.DecimalField(
        max_digits=40, decimal_places=2, blank=True, null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=255)

    def __str__(self) -> str:
        return f"{self.title}-{self.get_level_display()}"  # type: ignore

    def clean(self) -> None:
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("End date can not be before start date")
        self.update_active_status()

    def update_active_status(self):
        current_date = timezone.now().date()
        self.is_active = self.end_date > current_date

    @classmethod
    def update_all_active_statuses(cls):
        """Update the `is_active` of all subsidy programs in the database"""
        current_date = timezone.now().date()
        cls.objects.filter(end_date__lt=current_date, is_active=True).update(
            is_active=False
        )


class SubsidizedItem(TimeStampModel):
    class ItemType(models.TextChoices):
        SEED = "SEED", "Seed"
        FERTILIZER = "FERTILIZER", "Fertilizer"
        MECHANIZATION = "MECHANIZATION", "Mechanization"
        CHEMICAL = "AGROCHEMICAL", "Chemical"

    type = models.CharField(choices=ItemType.choices, max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    subsidized_item = GenericForeignKey("content_type", "object_id")  # content object
    item_price = models.DecimalField(max_digits=7, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ltr")

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

    def __str__(self):
        return f"{self.subsidized_item}"


class SubsidyRate(TimeStampModel):
    subsidy_program = models.ForeignKey(
        SubsidyProgram, related_name="subsidy_rate", on_delete=models.CASCADE
    )
    subsidized_item = models.ForeignKey(
        SubsidizedItem, related_name="subsidy_rate", on_delete=models.CASCADE
    )
    rate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal(50.0),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subsidy_program", "subsidized_item"],
                name="unique_subsidy_rate",
            )
        ]

    def __str__(self):
        return f"{self.subsidy_program.title}-{self.rate}"

    @property
    def subsidized_price(self):
        return self.subsidized_item.item_price * (1 - self.rate / 100)


class SubsidyInstance(models.Model):
    farmer = models.ForeignKey(
        Farmer, related_name="subsidy_intance", on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        SubsidizedItem,
        related_name="subsidy_intance",
        on_delete=models.CASCADE,
    )
    subsidy_program = models.ForeignKey(
        SubsidyProgram,
        related_name="subsidy_intance",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    redemption_date = models.DateField(auto_now_add=True)
    # Name of the redemption center.
    # The idea is to make all the major markets a redemption center, likewise the vendors
    redemption_location = models.CharField(max_length=255, null=True, blank=True)
    discounted_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        editable=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["farmer", "item", "subsidy_program"],
                name="unique_farmer_subsidy",
            )
        ]

    def __str__(self):
        return f"{self.id} - {self.item}"  # type: ignore

    @cached_property
    def item_unit(self):
        return self.item.unit

    def clean(self):
        from django.core.exceptions import ValidationError

        # Check if farmer is eligible for the program based on state
        if (
            self.subsidy_program.level == "STATE"
            and self.farmer.state_of_residence != self.subsidy_program.state
        ):
            raise ValidationError("Farmer is not eligible for this state program")

        # Check if farmer has already participated in a national and state program this year
        existing_instances = SubsidyInstance.objects.filter(
            farmer=self.farmer, subsidy_program__year=self.subsidy_program.end_date
        ).select_related("subsidy_program")

        national_count = sum(
            1
            for instance in existing_instances
            if instance.subsidy_program.level == "NATIONAL"
        )
        state_count = sum(
            1
            for instance in existing_instances
            if instance.subsidy_program.level == "STATE"
        )

        if self.subsidy_program.level == "NATIONAL" and national_count > 0:
            raise ValidationError(
                "Farmer has already participated in a national program this year."
            )
        elif self.subsidy_program.level == "STATE" and state_count > 0:
            raise ValidationError(
                "Farmer has already participated in a state program this year."
            )


class InputPriceHistory(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    effective_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.item}"
