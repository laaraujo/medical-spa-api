from model_bakery import baker


def test__returns_all_services(client, user):
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


def test__with_med_spa_query_param__filters_results(client, user):
    s1, s2, s3 = [baker.make("med_spa.Service") for _ in range(3)]
    client.force_authenticate(user)
    r = client.get(f"/services/?med_spa={s1.med_spa.id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["id"] == s1.id


def test__with_invalid_med_spa_query_param__returns_no_results(client, user):
    s1, s2, s3 = [baker.make("med_spa.Service") for _ in range(3)]
    client.force_authenticate(user)
    r = client.get(f"/services/?med_spa=333")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
