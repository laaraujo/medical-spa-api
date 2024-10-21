import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from med_spa import models
from model_bakery import baker


def get_csv_data(path: str) -> list[list[str]]:
    with open(path) as infile:
        reader = csv.reader(infile)
        _ = next(reader)[1:]  # remove headers
        return [row for row in reader]


def populate_local_dev_data():
    print("seeding db with fake medspas, services and appointments")
    med_spas = baker.make(models.MedicalSpa, _quantity=5)

    products = models.ServiceProduct.objects.all()

    for product in products:
        for med_spa in med_spas:
            services = baker.make(
                models.Service, product=product, med_spa=med_spa, _quantity=3
            )

            appt = baker.make(models.Appointment)
            appt.services.set(services)
    print("finished seeding db with fake data")


def populate_products(csv_data):
    print("creating service products")
    for row in csv_data:
        category, type, product, supplier = row

        service_product_provider = None
        if supplier and supplier != "--":
            service_product_provider, _ = (
                models.ServiceProductProvider.objects.get_or_create(name=supplier)
            )

        service_category, _ = models.ServiceCategory.objects.get_or_create(
            name=category
        )

        service_type, _ = models.ServiceType.objects.get_or_create(
            name=type, category=service_category
        )

        if product and product != "--":
            product_name = product
        else:
            product_name = (
                service_type.name
            )  # use the category's name if product name is not defined

        models.ServiceProduct.objects.get_or_create(
            name=product_name, type=service_type, provider=service_product_provider
        )
    print("finished creating service products")


class Command(BaseCommand):
    def handle(self, *args, **options):
        allowed_services = get_csv_data("med_spa/management/data/allowed_services.csv")
        populate_products(allowed_services)
        if settings.DEBUG:
            populate_local_dev_data()
