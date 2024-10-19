def test__returns_service(client, user, service):
    client.force_authenticate(user)
    r = client.get(f"/services/{service.id}/")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == service.id
    assert data["med_spa"] == service.med_spa.id
    assert data["product"] == service.product.id
    assert data["name"] == service.name
    assert data["description"] == service.description
    assert data["price"] == float(service.price)
    assert data["duration"] == service.duration


def test__with_anonymous_user__returns_401(client, service):
    r = client.get(f"/services/{service.id}/")
    assert r.status_code == 401


def test__invalid_id__returns_404(client, user):
    client.force_authenticate(user)
    r = client.get("/services/333/")
    assert r.status_code == 404
