from datetime import datetime

import pytest
from dateutil.parser import parse
from med_spa.exceptions import ApptEmptyServicesError
from med_spa.models import Appointment

from tests.utils import faker


def test__updates_appointment(client, user, appointment, service):
    payload = {
        "services": [service.id],
        "start_time": datetime.now(),
        "status": Appointment.STATUS.COMPLETED,
    }
    assert service not in appointment.services.all()
    assert appointment.status != payload["status"]
    client.force_authenticate(user)
    r = client.put(f"/appointments/{appointment.id}/", data=payload)
    assert r.status_code == 200
    appointment.refresh_from_db()
    assert appointment.services.count() == 1
    assert appointment.services.first() == service
    assert appointment.start_time.replace(tzinfo=None) == payload["start_time"]
    assert appointment.status == payload["status"]


def test__with_anonymous_user__returns_401(client, appointment):
    r = client.put(f"/appointments/{appointment.id}/", data={})
    assert r.status_code == 401


@pytest.mark.parametrize(
    "field, exception_cls",
    [
        ("services", ApptEmptyServicesError),
        ("start_time", None),
    ],
)
def test__with_missing_required_fields__returns_400(
    field, exception_cls, client, user, appointment, service
):
    payload = {
        "services": [service.id],
        "start_time": datetime.now(),
    }
    del payload[field]
    client.force_authenticate(user)
    r = client.put(f"/appointments/{appointment.id}/", data=payload)
    assert r.status_code == 400
    data = r.json()
    expected_msg = (
        exception_cls.default_detail if exception_cls else "This field is required."
    )
    assert data[field] == [expected_msg]
