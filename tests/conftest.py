import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APIClient


def pytest_collection_modifyitems(items):
    """
    Add `pytest.mark.django_db()` mark to ALL tests.
    https://docs.pytest.org/en/latest/reference/reference.html#pytest.hookspec.pytest_collection_modifyitems
    """
    for item in items:
        item.add_marker("django_db")


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return baker.make(User)