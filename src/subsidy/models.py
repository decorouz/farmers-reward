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

    manufacturer = models.CharField(max_length=100, unique=True)
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
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="50kg")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_fertilizer",
                fields=["manufacturer", "fertilizer_type", "fertilizer_blend"],
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
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="kg")
    price = models.DecimalField(max_digits=7, decimal_places=2)
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
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ha")
    price = models.DecimalField(max_digits=7, decimal_places=2)
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
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="ltr")
    price = models.DecimalField(max_digits=7, decimal_places=2)
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
                fields=["manufacturer", "agrochemical_type"],
                name="unique_agrochemical_manufacturer_type",
            )
        ]

    def __str__(self):
        return f"{self.manufacturer}({self.agrochemical_type})"


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
    target_num_of_beneficiaries = models.SmallIntegerField(
        default=200, validators=[MinValueValidator(1)]
    )
    current_num_of_beneficiaries = models.SmallIntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(Region, on_delete=models.CASCADE)
    budget_in_naira = models.DecimalField(
        max_digits=40, decimal_places=2, blank=True, null=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
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
        self.update_active_status()

    def update_active_status(self):
        current_date = timezone.now().date()
        self.is_active = self.end_date > current_date

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
    class ItemType(models.TextChoices):
        SEED = "SEED", "Seed"
        FERTILIZER = "FERTILIZER", "Fertilizer"
        MECHANIZATION = "MECHANIZATION", "Mechanization"
        CHEMICAL = "AGROCHEMICAL", "Chemical"

    type = models.CharField(choices=ItemType.choices, max_length=50)
    seed = models.OneToOneField(Seed, null=True, blank=True, on_delete=models.CASCADE)
    fertilizer = models.OneToOneField(
        Fertilizer, null=True, blank=True, on_delete=models.CASCADE
    )
    mechanization = models.OneToOneField(
        MechanizationOperation, null=True, blank=True, on_delete=models.CASCADE
    )
    chemical = models.OneToOneField(
        Agrochemical, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seed", "fertilizer", "mechanization", "chemical"],
                name="unique_subsidized_item",
            )
        ]

    def __str__(self):
        return f"{self.get_item()}"

    def get_item(self):
        if self.type == self.ItemType.SEED:
            return self.seed
        elif self.type == self.ItemType.FERTILIZER:
            return self.fertilizer
        elif self.type == self.ItemType.MECHANIZATION:
            return self.mechanization
        elif self.type == self.ItemType.CHEMICAL:
            return self.chemical
        return None

    @property
    def item_unit(self):
        item = self.get_item()
        return item.unit if item else ""

    @property
    def item_price(self):
        item = self.get_item()
        return item.price if item else 0


class SubsidyInstance(models.Model):
    class CropType(models.TextChoices):
        MAIZE = "MAIZE", "Maize"
        RICE = "RICE", "Rice"
        SOYBEAN = "SOYA", "Soybean"
        YAM = "YAM", "YAM"
        CASSAVA = "CASSAVA", "Cassava"
        CASHCROPS = "CASHCROPS", "Ginger, Cocoa, ..."

    farmer = models.ForeignKey(
        Farmer, related_name="subsidy_instance", on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        SubsidizedItem,
        related_name="subsidy_instance",
        on_delete=models.CASCADE,
    )
    subsidy_program = models.ForeignKey(
        SubsidyProgram,
        related_name="subsidy_instance",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    redemption_date = models.DateField(auto_now_add=True)
    redemption_location = models.CharField(max_length=255, null=True, blank=True)

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
        return self.item.item_unit

    def clean(self):
        validators.validate_farmer_eligibility(self.farmer, self.subsidy_program)

    @cached_property
    def subsidized_value(self):
        """Compute the value of subsidy based on the subsidy rate"""
        return (
            self.item.item_price * self.quantity * (1 - self.subsidy_program.rate / 100)
        )
