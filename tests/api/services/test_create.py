import pytest
from med_spa.models import Service
from model_bakery import baker

from tests.utils import faker


def test__creates_service(client, user, product, med_spa):
    payload = {
        "med_spa_id": med_spa.id,
        "product_id": product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": 45,
    }
    client.force_authenticate(user)
    r = client.post("/services/", data=payload)
    assert r.status_code == 201
    data = r.json()
    assert Service.objects.filter(id=data["id"]).exists()
    assert data["med_spa"] == payload["med_spa_id"]
    assert data["product"] == payload["product_id"]
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["duration"] == payload["duration"]


def test__with_anonymous_user__returns_401(client):
    r = client.post("/services/", data={})
    assert r.status_code == 401


@pytest.mark.parametrize(
    "field",
    [
        "med_spa_id",
        "product_id",
        "name",
        "description",
        "price",
        "duration",
    ],
)
def test__with_missing_required_fields__returns_400(
    field, client, user, product, med_spa
):
    payload = {
        "med_spa_id": med_spa.id,
        "product_id": product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": 45,
    }
    del payload[field]
    client.force_authenticate(user)
    r = client.post("/services/", data=payload)
    assert r.status_code == 400
    data = r.json()
    assert data[field] == ["This field is required."]


def test__with_triggered_unique_together_constraint__returns_409(
    client,
    user,
):
    service = baker.make(Service)
    payload = {
        "med_spa_id": service.med_spa.id,
        "product_id": service.product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": service.duration,
    }
    client.force_authenticate(user)
    r = client.post("/services/", data=payload)
    assert r.status_code == 409
