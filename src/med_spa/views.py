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
