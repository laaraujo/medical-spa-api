from decimal import Decimal

import pytest

from tests.utils import faker


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
def test__updates_field(field, client, user, service, product):
    base_payload = {
        "product_id": product.id,
        "name": faker.text(max_nb_chars=100),
        "description": faker.text(max_nb_chars=300),
        "price": 99.99,
        "duration": service.duration,
    }
    payload = {field: base_payload[field]}
    client.force_authenticate(user)
    r = client.patch(f"/services/{service.id}/", data=payload)
    assert r.status_code == 200
    service.refresh_from_db()
    val = getattr(service, field)
    if isinstance(val, Decimal):
        val = float(val)
    assert val == payload[field]


def test__cannot_update_med_spa(client, user, service, med_spa):
    client.force_authenticate(user)
    assert service.med_spa.id != med_spa.id
    r = client.patch(f"/services/{service.id}/", data={"med_spa_id": med_spa.id})
    service.refresh_from_db()
    assert r.status_code == 200
    assert service.med_spa.id != med_spa.id


def test__with_anonymous_user__returns_401(client, service):
    r = client.patch(f"/services/{service.id}/", data={})
    assert r.status_code == 401
