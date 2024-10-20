from dateutil.parser import parse


def test__returns_appointment(client, user, appointment):
    client.force_authenticate(user)
    r = client.get(f"/appointments/{appointment.id}/")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == appointment.id
    assert data["user"] == appointment.user.id
    assert data["status"] == appointment.status
    assert data["total_duration"] == appointment.total_duration
    assert data["total_price"] == float(appointment.total_price)
    assert parse(data["start_time"]) == appointment.start_time


def test__with_anonymous_user__returns_401(client, service):
    r = client.get(f"/appointments/{service.id}/")
    assert r.status_code == 401


def test__invalid_id__returns_404(client, user):
    client.force_authenticate(user)
    r = client.get("/appointments/333/")
    assert r.status_code == 404
