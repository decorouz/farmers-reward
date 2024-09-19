from decimal import Decimal

from cities_light.models import Country, Region
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.forms import ValidationError
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify

from core.models import BaseModel, TimeStampModel
from farmers.models import Farmer
from subsidy import validators

# Define choices for units
UNIT_CHOICES = [
    ("kg", "kilogram"),
    ("50kg", "50 kilogram"),
    ("ltr", "liter"),
    ("ha", "hectare"),
]


class Fertilizer(TimeStampModel):
    class FertilizerChoice(models.TextChoices):
        NPK = "NPK", "Npk"
        UREA = "UREA", "Urea"
        PHOSPHATE = "SSP", "Single Super Phosphate"
        POTASH = "MOP", "Muriate of Potash"
        OTHER = "OTHER", "Others"

    manufacturer = models.CharField(max_length=100)
    fertilizer_type = models.CharField(
        max_length=5,
        choices=FertilizerChoice.choices,
        default=FertilizerChoice.NPK,
    )
    fertilizer_blend = models.CharField(
        max_length=20,
        default="20:10:10",
        validators=[
            RegexValidator(r"^\d+:\d+:\d+$", "Invalid fertilizer blend format")
        ],
    )
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="50kg")
    # price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manufacturer", "fertilizer_type", "fertilizer_blend"],
                name="unique_fertilizer",
                condition=Q(manufacturer__iexact=Lower("manufacturer")),
            )
        ]

    def __str__(self):
        return f"{self.manufacturer}-{self.fertilizer_type}-{self.fertilizer_blend}"


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

    seed_company = models.CharField(max_length=100, default="Seedco")
    crop = models.CharField(
        max_length=20,
        choices=CropChoice.choices,
        default=CropChoice.MAIZE,
    )
    seed_variety = models.CharField(max_length=255, null=True, blank=True)
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="kg")
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    gmo = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    seed_variety__iexact=Lower("seed_variety"),
                ),
                fields=["seed_company", "crop", "seed_variety"],
                name="unique_seed",
            )
        ]

    def __str__(self):
        return f"{self.seed_company}-{self.crop}-{self.seed_variety}"


class MechanizationOperation(TimeStampModel):
    OPERATION_TYPES = [
        ("PLOWING", "Plowing"),
        ("HARVESTING", "Harvesting"),
        ("PLANTING", "Planting"),
        ("SPRAYING", "Spraying"),
        ("TILLING", "Tilling"),
        ("FERTILIZING", "Fertilizing"),
        ("IRRIGATING", "Irrigating"),
        ("OTHER", "Other"),
    ]
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ha")
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    operation_type = models.CharField(
        max_length=20, choices=OPERATION_TYPES, default="PLOWING"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["operation_type"],
                name="unique_mechanization_operation",
            )
        ]

    def __str__(self):
        return f"{self.get_operation_type_display()}-per-{self.unit}"  # type: ignore


class Agrochemical(TimeStampModel):
    class AgrochemicalChoice(models.TextChoices):
        PRE_EMERGENCE = "PRE", "Pre Emergence Herbicide"
        POST_EMERGENCE = "POS", "Post Emergence Herbicide"
        PESTICIDE = "PES", "Pesticide"
        INSECTICIDE = "INT", "Insecticide"

    manufacturer = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    # unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ltr")
    # price = models.DecimalField(max_digits=7, decimal_places=2)
    agrochemical_type = models.CharField(
        max_length=3,
        choices=AgrochemicalChoice.choices,
        default=AgrochemicalChoice.PRE_EMERGENCE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                condition=Q(
                    manufacturer__iexact=Lower("manufacturer"),
                ),
                fields=["manufacturer", "name", "agrochemical_type"],
                name="unique_agrochemical_manufacturer_type",
            )
        ]

    def __str__(self):
        return f"{self.manufacturer}({self.name})"


class Program(BaseModel):
    class ProgramLevel(models.TextChoices):
        STATE = "STATE", "State"
        NATIONAL = "NATIONAL", "National"

    title = models.CharField(max_length=255)
    implementation_details = models.TextField(null=True, blank=True)
    program_sponsor = models.CharField(max_length=255, default="Federal Government")
    level = models.CharField(
        max_length=10, choices=ProgramLevel.choices, default=ProgramLevel.NATIONAL
    )
    current_num_of_beneficiaries = models.SmallIntegerField(default=0, editable=False)

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(Region, on_delete=models.CASCADE)
    budget_in_naira = models.DecimalField(
        default=Decimal("7000000000.00"),
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=False, null=False)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["-start_date"]
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self) -> str:
        return f"{self.get_level_display()}-{self.title}"  # type: ignore

    @property
    def year(self):
        return self.end_date.year

    def clean(self) -> None:
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError("End date can not be before start date")

    # def update_active_status(self):
    #     current_date = timezone.now().date()
    #     self.is_active = self.end_date > current_date

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.clean()  # Ensure validation runs before saving
        super().save(*args, **kwargs)


# ===== Input base subsidy program ======


class SubsidyProgram(Program):
    rate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )


class SubsidizedItem(TimeStampModel):
    ITEM_TYPES = [
        ("FERTILIZER", "Fertilizer"),
        ("SEED", "Seed"),
        ("AGROCHEMICAL", "Agrochemical"),
        ("MECHANIZATION", "Mechanization"),
    ]

    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)

    # Foreign Key relationships
    fertilizer = models.ForeignKey(
        Fertilizer, on_delete=models.SET_NULL, null=True, blank=True
    )
    seed = models.ForeignKey(Seed, on_delete=models.SET_NULL, null=True, blank=True)
    agrochemical = models.ForeignKey(
        Agrochemical, on_delete=models.SET_NULL, null=True, blank=True
    )
    mechanization_operation = models.ForeignKey(
        MechanizationOperation, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item_type", "item_name"], name="unique_subsidized_item"
            )
        ]

    def __str__(self):
        return f"{self.get_item_type_display()} - {self.item_name}"

    def clean(self):
        super().clean()
        if self.item_type == "FERTILIZER" and not self.fertilizer:
            raise ValidationError(
                "Fertilizer must be specified for fertilizer item type."
            )
        elif self.item_type == "SEED" and not self.seed:
            raise ValidationError("Seed must be specified for seed item type.")
        elif self.item_type == "AGROCHEMICAL" and not self.agrochemical:
            raise ValidationError(
                "Agrochemical must be specified for agrochemical item type."
            )
        elif self.item_type == "MECHANIZATION" and not self.mechanization_operation:
            raise ValidationError(
                "Mechanization operation must be specified for mechanization item type."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class SubsidyInstance(models.Model):
    farmer = models.ForeignKey(
        Farmer, related_name="subsidy_instances", on_delete=models.CASCADE
    )
    subsidy_program = models.ForeignKey(
        SubsidyProgram,
        related_name="subsidy_instances",
        on_delete=models.CASCADE,
    )
    redemption_date = models.DateField(auto_now_add=True)
    redemption_location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["farmer", "subsidy_program"],
                name="unique_farmer_subsidy",
            )
        ]

    def __str__(self):
        return f"Subsidy for {self.farmer} under {self.subsidy_program}"

    def clean(self):
        validators.validate_farmer_eligibility(self.farmer, self.subsidy_program)

    @property
    def subsidized_value(self):
        """Compute the total subsidized value for all items in this instance"""
        return sum(item.subsidized_value for item in self.subsidy_instance_items.all())


class SubsidyInstanceItem(models.Model):
    subsidy_instance = models.ForeignKey(
        SubsidyInstance, related_name="subsidy_instance_items", on_delete=models.CASCADE
    )
    subsidized_item = models.ForeignKey(
        SubsidizedItem, related_name="subsidy_instance_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("subsidy_instance", "subsidized_item")

    def __str__(self):
        return (
            f"{self.subsidized_item} (Qty: {self.quantity}) for {self.subsidy_instance}"
        )

    @property
    def subsidized_value(self):
        """Compute the subsidized value for this specific item"""
        subsidy_rate = self.subsidy_instance.subsidy_program.rate
        return (
            self.subsidized_item.item_price * self.quantity * (1 - subsidy_rate / 100)
        )
