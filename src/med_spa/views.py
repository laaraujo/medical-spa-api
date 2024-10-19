from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from med_spa import models, serializers


class ServiceViewSet(ModelViewSet):
    queryset = models.Service.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.ServiceUpdateSerializer
        return serializers.ServiceSerializer

    def get_queryset(self):
        queryset = models.Service.objects.all()
        med_spa = self.request.query_params.get("med_spa")
        if med_spa is not None:
            queryset = queryset.filter(med_spa__id=med_spa)
        return queryset
