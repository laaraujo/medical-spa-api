from django.shortcuts import get_object_or_404
from rest_framework import serializers

from med_spa import models


class ServiceSerializer(serializers.ModelSerializer):
    med_spa = serializers.PrimaryKeyRelatedField(read_only=True)
    med_spa_id = serializers.IntegerField(write_only=True)

    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    def validate_product_id(self, value):
        """
        Check provided related product_id exists (possible 404)
        """
        get_object_or_404(models.ServiceProduct, id=value)
        return value

    def validate_med_spa_id(self, value):
        """
        Check provided related med_spa_id exists (possible 404)
        """
        get_object_or_404(models.MedicalSpa, id=value)
        return value

    class Meta:
        model = models.Service
        fields = "__all__"


class ServiceUpdateSerializer(ServiceSerializer):
    med_spa = None
    med_spa_id = None

    class Meta:
        model = models.Service
        exclude = ["med_spa"]
