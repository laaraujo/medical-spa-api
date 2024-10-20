from datetime import datetime
from decimal import Decimal

import pytest
from med_spa.models import Appointment

from tests.utils import faker


def test__updates_appointment_services(client, user, appointment, service):
    payload = {"services": [service.id]}
    assert service not in appointment.services.all()
    client.force_authenticate(user)
    r = client.patch(f"/appointments/{appointment.id}/", data=payload)
    assert r.status_code == 200
    appointment.refresh_from_db()
    assert appointment.services.count() == 1
    assert service == appointment.services.first()


def test__updates_appointment_start_time(client, user, appointment):
    payload = {"start_time": datetime.now()}
    assert appointment.start_time.replace(tzinfo=None) != payload["start_time"]
    client.force_authenticate(user)
    r = client.patch(f"/appointments/{appointment.id}/", data=payload)
    assert r.status_code == 200
    appointment.refresh_from_db()
    assert appointment.start_time.replace(tzinfo=None) == payload["start_time"]


def test__updates_appointment_status(client, user, appointment):
    payload = {"status": Appointment.STATUS.CANCELED}
    assert appointment.status != payload["status"]
    client.force_authenticate(user)
    r = client.patch(f"/appointments/{appointment.id}/", data=payload)
    assert r.status_code == 200
    appointment.refresh_from_db()
    assert appointment.status == payload["status"]


def test__with_anonymous_user__returns_401(client, appointment):
    r = client.patch(f"/appointments/{appointment.id}/", data={})
    assert r.status_code == 401
