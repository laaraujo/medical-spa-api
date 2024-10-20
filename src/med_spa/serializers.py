from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers

from med_spa import exceptions, models


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


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    services = serializers.PrimaryKeyRelatedField(
        queryset=models.Service.objects.all().prefetch_related("med_spa"),
        required=True,
        many=True,
    )

    total_duration = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def validate_services(self, value):
        """
        Check provided service ids for:
        - Must be one or more
        - All services must exist (implicit with PrimaryKeyRelatedField)
        - All must belong to the same med spa

        Then return actual models.Service instances instead of plain ids
        """

        services = value

        if not services:  # more than one
            raise exceptions.ApptEmptyServicesError

        med_spas = {s.med_spa for s in services}

        if len(med_spas) != 1:  # must be of same med spa
            raise exceptions.MultiMedSpaApptError

        return services

    def create(self, validated_data):
        services = validated_data.pop("services", [])
        appointment = models.Appointment.objects.create(**validated_data)
        appointment.services.set(services)
        return appointment

    def update(self, instance, validated_data):
        services = validated_data.pop("services", None)
        instance = super().update(instance, validated_data)

        if services is not None:
            instance.services.set(services)  # Update the services
        return instance

    def get_total_duration(self, obj):
        return obj.total_duration

    def get_total_price(self, obj):
        return obj.total_price

    class Meta:
        model = models.Appointment
        fields = [
            "id",
            "services",
            "user",
            "start_time",
            "status",
            "total_duration",
            "total_price",
            "created",
            "updated",
        ]
