from model_bakery import baker


def test_returns_all_services(client, user):
    services = [baker.make("med_spa.Service") for _ in range(3)]
    client.force_authenticate(user)
    r = client.get("/services/")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 3
    ids = [s["id"] for s in data]
    for service in services:
        assert service.id in ids


def test__with_anonymous_user__returns_401(client):
    r = client.get("/services/")
    assert r.status_code == 401
