from unittest import mock

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# logout


def test_logout_requires_login(client):
    url = reverse("users:logout")
    response = client.get(url)
    assert response.status_code == 302


def test_logout_returns_302(auth_client):
    url = reverse("users:logout")
    response = auth_client.get(url)
    assert response.status_code == 302


# reset_user_avatar


def test_reset_avatar_requires_login(client):
    url = reverse("users:reset_avatar")
    response = client.post(url)
    assert response.status_code == 302


def test_reset_avatar_returns_200(auth_client):
    url = reverse("users:reset_avatar")
    response = auth_client.post(url)
    assert response.status_code == 200
    assert "avatar_url" in response.json()


def test_avatar_throttling(auth_client):
    url = reverse("users:reset_avatar")
    with mock.patch(
        "core.services.throttling.endpoint.is_throttled", return_value=True
    ):
        response = auth_client.post(url)
    assert response.status_code == 429
