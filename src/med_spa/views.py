from dateutil.parser import parse
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from med_spa import exceptions, models, serializers


class ServiceViewSet(ModelViewSet):
    queryset = models.Service.objects.all().prefetch_related("med_spa", "product")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return serializers.ServiceUpdateSerializer
        return serializers.ServiceSerializer

    def get_queryset(self):
        queryset = self.queryset
        med_spa = self.request.query_params.get("med_spa")
        if med_spa is not None:
            try:
                queryset = queryset.filter(med_spa__id=med_spa)
            except ValueError:
                raise exceptions.InvalidMedSpaId
        return queryset


class AppointmentViewSet(ModelViewSet):
    queryset = models.Appointment.objects.all().prefetch_related("services", "user")
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset

        start_date = self.request.query_params.get("start_date")
        if start_date is not None:
            try:
                queryset = queryset.filter(start_time__date=start_date)
            except ValidationError:
                raise exceptions.InvalidStartDateError

        status = self.request.query_params.get("status")

        if status is not None:
            if status not in models.Appointment.STATUS.values:
                raise exceptions.InvalidStatusError
            queryset = queryset.filter(status=status)

        return queryset
