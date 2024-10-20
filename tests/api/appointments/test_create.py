from datetime import datetime

import pytest
from med_spa.exceptions import ApptEmptyServicesError, MultiMedSpaApptError
from med_spa.models import Appointment, Service
from model_bakery import baker


def test__creates_appointment(client, user, service):
    payload = {
        "services": [service.id],
        "start_time": datetime.now(),
        "status": Appointment.STATUS.COMPLETED,
    }
    client.force_authenticate(user)
    r = client.post(f"/appointments/", data=payload)
    assert r.status_code == 201
    data = r.json()
    appt = Appointment.objects.get(id=data["id"])
    assert data["id"] == appt.id
    assert user == appt.user
    assert payload["status"] == appt.status
    assert payload["start_time"] == appt.start_time.replace(tzinfo=None)

    assert len(payload["services"]) == appt.services.count()
    assert payload["services"][0] == appt.services.first().id


def test__with_empty_services__returns_400(client, user):
    payload = {
        "services": [],
        "start_time": datetime.now(),
        "status": Appointment.STATUS.COMPLETED,
    }
    client.force_authenticate(user)
    r = client.post(f"/appointments/", data=payload)
    assert r.status_code == 400
    assert r.json()["services"] == [ApptEmptyServicesError.default_detail]


def test__with_services_from_diff_med_spa__returns_400(client, user, service):
    diff_med_spa_service = baker.make(Service)
    assert diff_med_spa_service.med_spa != service.med_spa
    payload = {
        "services": [service.id, diff_med_spa_service.id],
        "start_time": datetime.now(),
        "status": Appointment.STATUS.COMPLETED,
    }
    client.force_authenticate(user)
    r = client.post(f"/appointments/", data=payload)
    assert r.status_code == 400
    assert r.json()["services"] == [MultiMedSpaApptError.default_detail]


def test__with_invalid_services__returns_400(client, user):
    payload = {
        "services": [333],
        "start_time": datetime.now(),
        "status": Appointment.STATUS.COMPLETED,
    }
    client.force_authenticate(user)
    r = client.post(f"/appointments/", data=payload)
    assert r.status_code == 400


def test__with_anonymous_user__returns_401(client):
    r = client.post(f"/appointments/", data={})
    assert r.status_code == 401


def test__with_missing_optional_fields__creates_appointment(client, user, service):
    payload = {
        "services": [service.id],
        "start_time": datetime.now(),
        # no status
    }
    client.force_authenticate(user)
    r = client.post(f"/appointments/", data=payload)
    assert r.status_code == 201
    appt = Appointment.objects.get(id=r.json()["id"])
    assert appt.status == Appointment.STATUS.SCHEDULED


@pytest.mark.parametrize(
    "field, exception_cls",
    [
        ("services", ApptEmptyServicesError),
        ("start_time", None),
    ],
)
def test__with_missing_required_fields__returns_400(
    field, exception_cls, client, user, service
):
    payload = {
        "services": [service.id],
        "start_time": datetime.now(),
    }
    del payload[field]
    client.force_authenticate(user)
    r = client.post("/appointments/", data=payload)
    assert r.status_code == 400
    data = r.json()
    expected_msg = (
        exception_cls.default_detail if exception_cls else "This field is required."
    )
    assert data[field] == [expected_msg]
