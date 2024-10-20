from datetime import datetime, timedelta

from med_spa.exceptions import InvalidStartDateError, InvalidStatusError
from med_spa.models import Appointment
from model_bakery import baker


def test__returns_all_appts(client, user):
    appts = [baker.make("med_spa.Appointment") for _ in range(3)]
    client.force_authenticate(user)
    r = client.get("/appointments/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3
    ids = [s["id"] for s in data]
    for appt in appts:
        assert appt.id in ids


def test__with_anonymous_user__returns_401(client):
    r = client.get("/appointments/")
    assert r.status_code == 401


def test__with_start_date_query_param__filters_results(client, user):
    appt = baker.make("med_spa.Appointment")
    _ = baker.make("med_spa.Appointment", start_time=datetime.now() + timedelta(days=1))
    client.force_authenticate(user)
    date = appt.start_time.date()
    r = client.get(f"/appointments/?start_date={date}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == appt.id


def test__with_invalid_start_date_query_param__returns_400(client, user):
    _ = [baker.make("med_spa.Appointment") for _ in range(3)]
    client.force_authenticate(user)
    r = client.get(f"/appointments/?start_date=333")
    assert r.status_code == 400
    assert r.json()["detail"] == InvalidStartDateError.default_detail


def test__with_status_query_param__filters_results(client, user):
    appt = baker.make("med_spa.Appointment", status=Appointment.STATUS.CANCELED)
    _ = baker.make("med_spa.Appointment", status=Appointment.STATUS.COMPLETED)
    client.force_authenticate(user)
    r = client.get(f"/appointments/?status={appt.status}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == appt.id


def test__with_invalid_status_query_param__returns_400(client, user):
    client.force_authenticate(user)
    r = client.get(f"/appointments/?status=333")
    assert r.status_code == 400
    assert r.json()["detail"] == InvalidStatusError.default_detail
