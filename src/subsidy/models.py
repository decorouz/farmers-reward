from decimal import Decimal

from cities_light.models import Country, Region
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import F, Q, Sum
from django.db.models.functions import Lower
from django.forms import ValidationError
from django.utils.text import slugify

from farmers.models import Farmer


class Subsidy(models.Model):
    class ProgramLevel(models.TextChoices):
        STATE = "STATE", "State"
        NATIONAL = "NATIONAL", "National"

    title = models.CharField(max_length=255)
    implementation_details = models.TextField(default="")
    program_sponsor = models.CharField(max_length=255, default="Federal Government")
    level = models.CharField(
        max_length=10, choices=ProgramLevel.choices, default=ProgramLevel.NATIONAL
    )
    current_num_of_beneficiaries = models.SmallIntegerField(default=0, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(Region, on_delete=models.CASCADE)
    budget_in_naira = models.DecimalField(
        default=Decimal("10"),
        max_digits=40,
        decimal_places=2,
    )
    rate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=Decimal(50.0),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Subsidy Program"
        verbose_name_plural = "Subsidy Programs"

    def __str__(self) -> str:
        return f"{self.get_level_display()}-{self.title}"

    @property
    def year(self):
        return self.end_date.year

    def clean(self) -> None:
        super().clean()
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("Start date cannot be after end date.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.clean()
        super().save(*args, **kwargs)


class SubsidyCategory(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="Name must be in the format 'CropSeason', e.g., 'MaizeWetSeason'.",
    )
    subsidies = models.ManyToManyField(Subsidy, through="SubsidyInstance")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=Q(
                    name__iexact=Lower("name"),
                ),
                name="unique_subsidy_category_name",
            )
        ]

    def __str__(self):
        return self.name


class InputCollection(models.Model):
    class CollectionType(models.TextChoices):
        FERTILIZER = "F", "Fertilizer"
        CHEMICAL = "C", "Agro chemicals"
        SEED = "S", "Certified seeds"
        MECHANIZATION = "M", "Mechanized Operations"

    type = models.CharField(
        max_length=1, choices=CollectionType.choices, default=CollectionType.FERTILIZER
    )

    def __str__(self):
        return self.get_type_display()


class AgriculturalInput(models.Model):
    class UnitChoice(models.TextChoices):
        KG = "KG", "Kilogram"
        BAG = "50KG", "50kg bag"
        LITER = "LTR", "Liter"
        HECTARE = "HA", "Hectare"
        ACRE = "AC", "Acre"

    company = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    collection = models.ForeignKey(InputCollection, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(
        max_length=5, choices=UnitChoice.choices, default=UnitChoice.BAG
    )
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "company"],
                name="unique_input",
                condition=Q(
                    company__iexact=Lower("company"), name__iexact=Lower("name")
                ),
            )
        ]

    def __str__(self):
        return f"{self.company}-{self.name}"

    def clean(self):
        if self.unit_price <= 0:
            raise ValidationError("Unit price must be greater than zero.")


class SubsidyInstance(models.Model):
    subsidy = models.ForeignKey(
        Subsidy, models.CASCADE, related_name="subsidy_instance"
    )
    category = models.ForeignKey(
        SubsidyCategory, models.PROTECT, related_name="subsidy"
    )
    agricultural_input = models.ForeignKey(
        AgriculturalInput, models.CASCADE, related_name="+"
    )
    quantity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(0)]
    )
    instance_rate = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("50.0"),
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subsidy", "category", "agricultural_input"],
                name="unique_subsidy_instance",
            )
        ]

    def __str__(self):
        return f"{self.subsidy.__str__()} - {self.category.__str__()}"

    @property
    def subsidized_unit_price(self):
        """
        Calculate the subsidized value for each input in this subsidy instance.
        """
        rate = (
            self.instance_rate
            if self.subsidy.rate == Decimal(0.0)
            else self.subsidy.rate
        )
        return self.agricultural_input.unit_price * (rate / Decimal(100))


class SubsidyApplication(models.Model):
    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name="application",
        limit_choices_to={"is_verified": True},
    )
    subsidy = models.ForeignKey(
        Subsidy, on_delete=models.CASCADE, related_name="subsidy_application"
    )
    category = models.ForeignKey(
        SubsidyCategory, models.CASCADE, related_name="application"
    )
    application_date = models.DateTimeField(auto_now_add=True)
    approval_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
        editable=False,
    )
    rejection_reason = models.TextField(blank=True)

    class Meta:
        unique_together = (
            "farmer",
            "subsidy",
        )

    def __str__(self):
        return f"{self.farmer} - {self.subsidy} - {self.application_date}"

    def save(self, *args, **kwargs):
        if self.approval_status == "pending":
            try:
                if self.farmer.is_verified:
                    self.approval_status = "approved"
                else:
                    self.approval_status = "rejected"
                    self.rejection_reason = "Applicant is not a verified farmer. Additional verification is required."
            except Farmer.DoesNotExist:
                self.approval_status = "rejected"
                self.rejection_reason = "Applicant is not registered as a farmer."
        super().save(*args, **kwargs)


class SubsidyDisbursement(models.Model):
    application = models.OneToOneField(
        SubsidyApplication,
        on_delete=models.CASCADE,
        related_name="disbursement",
        limit_choices_to={"approval_status": "approved"},
    )
    disbursement_date = models.DateField()

    total_value_items = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, editable=False
    )
    subsidized_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, editable=False
    )

    def clean(self):
        if self.subsidized_amount is not None and self.subsidized_amount <= 0:
            raise ValidationError("Amount disbursed must be greater than zero.")

    def save(self, *args, **kwargs):
        self.application.subsidy.current_num_of_beneficiaries += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Disbursement for {self.application} on {self.disbursement_date}: {self.subsidized_amount}"
