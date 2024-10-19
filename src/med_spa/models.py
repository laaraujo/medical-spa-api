from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


class BaseModel(models.Model):
    """
    Base model class implementing the usual audit-related fields
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        abstract = True


class MedicalSpa(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email_address = models.EmailField()

    class Meta:
        verbose_name = "Medical Spa"


class ServiceProductProvider(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Service Product Provider"


class ServiceCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"


class ServiceType(BaseModel):
    category = models.ForeignKey(
        "med_spa.ServiceCategory", related_name="types", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Service Type"
        unique_together = ("category", "name")


class ServiceProduct(BaseModel):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(
        "med_spa.ServiceType", related_name="products", on_delete=models.CASCADE
    )
    provider = models.ForeignKey(
        "med_spa.ServiceProductProvider",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = "Service Product"
        unique_together = ("name", "type")


class Service(BaseModel):
    med_spa = models.ForeignKey(
        "med_spa.MedicalSpa", related_name="services", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "med_spa.ServiceProduct", related_name="services", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    duration = models.IntegerField()  # To be represented in minutes

    class Meta:
        unique_together = (
            "med_spa",
            "product",
            "duration",
        )  # We don't need to confuse end users with duplicate options


class Appointment(BaseModel):
    services = models.ManyToManyField("med_spa.Service", related_name="appointments")
    user = models.ForeignKey(
        get_user_model(), related_name="appointments", on_delete=models.CASCADE
    )

    class STATUS(models.TextChoices):
        SCHEDULED = "scheduled"
        COMPLETED = "completed"
        CANCELED = "canceled"

    start_time = models.DateTimeField()
    status = models.CharField(
        choices=STATUS.choices, default=STATUS.SCHEDULED, max_length=20
    )

    @property
    def total_duration(self):
        return sum(service.duration for service in self.services.all())

    @property
    def total_price(self):
        return sum(service.price for service in self.services.all())
