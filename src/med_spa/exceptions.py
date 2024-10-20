from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import exception_handler

from med_spa.models import Appointment


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        response = Response(status=status.HTTP_409_CONFLICT)

    return response


class ApptEmptyServicesError(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Appointment must include at least one service"
    default_code = "missing_service"


class MultiMedSpaApptError(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "All services must belong to the same medical spa"
    default_code = "multi_med_spa_service"


class InvalidStartDateError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid start_date parameter provided"
    default_code = "invalid_date"


class InvalidStatusError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = f"Invalid status parameter provided, possible values are {Appointment.STATUS.values}"
    default_code = "invalid_status"


class InvalidMedSpaId(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid med_spa parameter provided, must be an integer value"
    default_code = "invalid_id"
