import pytest

from tests.utils import faker


def test__updates_service(client, user, service, product):
    payload = {
        "product_id": product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": 47,
    }
    client.force_authenticate(user)
    r = client.put(f"/services/{service.id}/", data=payload)
    assert r.status_code == 200
    service.refresh_from_db()
    assert service.product.id == payload["product_id"]
    assert service.name == payload["name"]
    assert service.description == payload["description"]
    assert float(service.price) == payload["price"]
    assert service.duration == payload["duration"]


def test__with_anonymous_user__returns_401(client, service):
    r = client.put(f"/services/{service.id}/", data={})
    assert r.status_code == 401


@pytest.mark.parametrize(
    "field",
    [
        "product_id",
        "name",
        "description",
        "price",
        "duration",
    ],
)
def test__with_missing_required_fields__returns_400(
    field, client, user, service, product
):
    payload = {
        "product_id": product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": 45,
    }
    del payload[field]
    client.force_authenticate(user)
    r = client.put(f"/services/{service.id}/", data=payload)
    assert r.status_code == 400
    data = r.json()
    assert data[field] == ["This field is required."]
