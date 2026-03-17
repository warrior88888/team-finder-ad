from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest_django.asserts import assertRedirects

if TYPE_CHECKING:
    from users.models import User as UserModel


pytestmark = pytest.mark.django_db


@pytest.fixture
def login_url():
    path = settings.LOGIN_URL
    return reverse(path)


@pytest.fixture
def login_redirect_url():
    path = settings.LOGIN_REDIRECT_URL
    return reverse(path)


User = get_user_model()


# UserDetailView


def test_user_detail_returns_200_for_anonymous(client, user):
    url = reverse("users:user_detail", kwargs={"pk": user.pk})
    response = client.get(url)
    assert response.status_code == 200


def test_user_detail_returns_200(user, auth_client):
    url = reverse("users:user_detail", kwargs={"pk": user.pk})
    response = auth_client.get(url)
    assert response.status_code == 200


def test_user_detail_returns_404_for_missing_user(auth_client):
    url = reverse("users:user_detail", kwargs={"pk": 99999})
    response = auth_client.get(url)
    assert response.status_code == 404


# UserListView


def test_user_list_returns_200_for_anonymous(client):
    url = reverse("users:user_list")
    response = client.get(url)
    assert response.status_code == 200


def test_user_list_returns_200_for_authenticated(auth_client):
    url = reverse("users:user_list")
    response = auth_client.get(url)
    assert response.status_code == 200


# UserRegisterView


def test_register_view_get_returns_200(client):
    url = reverse("users:register")
    response = client.get(url)
    assert response.status_code == 200


def test_register_view_valid_post_returns_302(
    client, user_register_form_data, login_redirect_url
):
    url = reverse("users:register")
    response = client.post(url, data=user_register_form_data)
    assertRedirects(response, login_redirect_url)


def test_register_view_invalid_post_returns_200(client):
    url = reverse("users:register")
    response = client.post(url, data={"email": "bad"})
    assert response.status_code == 200


# UserLoginView


def test_login_view_get_returns_200(client, login_url):
    response = client.get(login_url)
    assert response.status_code == 200


def test_login_view_valid_post_returns_302(
    client, user, login_url, login_redirect_url, password
):
    response = client.post(login_url, data={"email": user.email, "password": password})
    assertRedirects(response, login_redirect_url)


def test_login_view_invalid_post_returns_200(client, user, login_url, fake_password):
    response = client.post(
        login_url, data={"email": user.email, "password": fake_password}
    )
    assert response.status_code == 200


# UserEditView


def test_edit_view_requires_login(client):
    url = reverse("users:edit_profile")
    response = client.get(url)
    assert response.status_code == 302


def test_edit_view_returns_200(auth_client):
    url = reverse("users:edit_profile")
    response = auth_client.get(url)
    assert response.status_code == 200


def test_edit_view_valid_post_returns_302(auth_client, user_profile_form_data):
    url = reverse("users:edit_profile")
    response = auth_client.post(url, data=user_profile_form_data)
    user = cast("UserModel", User.objects.last())
    expected_url = reverse("users:user_detail", kwargs={"pk": user.pk})
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    ("field", "value"),
    [("github_url", "foo"), ("phone", "bar"), ("avatar", "baz")],
)
def test_edit_view_invalid_post_returns_200(auth_client, field, value):
    url = reverse("users:edit_profile")
    response = auth_client.post(url, data={field: value})
    assert response.status_code == 200


# UserPasswordChangeView


def test_password_change_requires_login(client):
    url = reverse("users:change_password")
    response = client.get(url)
    assert response.status_code == 302


def test_password_change_returns_200(auth_client):
    url = reverse("users:change_password")
    response = auth_client.get(url)
    assert response.status_code == 200


def test_password_change_invalid_post_returns_200(auth_client):
    url = reverse("users:change_password")
    response = auth_client.post(url, data={"old_password": "foo"})
    assert response.status_code == 200


def test_password_change_valid_post_returns_302(
    auth_client, user, password, fake_password
):
    url = reverse("users:change_password")
    response = auth_client.post(
        url,
        data={
            "old_password": password,
            "new_password1": fake_password,
            "new_password2": fake_password,
        },
    )
    expected_url = reverse("users:user_detail", kwargs={"pk": user.pk})
    assertRedirects(response, expected_url)
