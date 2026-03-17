from typing import cast

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from projects.models import Project

pytestmark = pytest.mark.django_db


# ProjectListView


def test_project_list_returns_200_for_anonymous(client):
    url = reverse("projects:projects_list")
    response = client.get(url)
    assert response.status_code == 200


def test_project_list_returns_200_for_authenticated(auth_client):
    url = reverse("projects:projects_list")
    response = auth_client.get(url)
    assert response.status_code == 200


# ProjectDetailView


def test_project_detail_returns_200(client, project):
    url = reverse("projects:project_detail", kwargs={"pk": project.pk})
    response = client.get(url)
    assert response.status_code == 200


def test_project_detail_returns_404_for_missing(client):
    url = reverse("projects:project_detail", kwargs={"pk": 99999})
    response = client.get(url)
    assert response.status_code == 404


# ProjectCreateView


def test_project_create_requires_login(client):
    url = reverse("projects:create_project")
    response = client.get(url)
    assert response.status_code == 302


def test_project_create_returns_200(auth_client):
    url = reverse("projects:create_project")
    response = auth_client.get(url)
    assert response.status_code == 200


def test_project_create_valid_post_returns_302(auth_client, project_form_data):
    url = reverse("projects:create_project")
    response = auth_client.post(url, data=project_form_data)
    project = cast("Project", Project.objects.last())
    expected_url = reverse("projects:project_detail", kwargs={"pk": project.pk})
    assertRedirects(response, expected_url)


def test_project_create_invalid_post_returns_200(auth_client):
    url = reverse("projects:create_project")
    response = auth_client.post(url, data={"foo": "bar"})
    assert response.status_code == 200


# ProjectUpdateView


def test_project_update_requires_login(client, project):
    url = reverse("projects:edit_project", kwargs={"pk": project.pk})
    response = client.get(url)
    assert response.status_code == 302


def test_project_update_returns_404_for_missing(auth_client):
    url = reverse("projects:edit_project", kwargs={"pk": 99999})
    response = auth_client.get(url)
    assert response.status_code == 404


def test_project_update_returns_200_for_owner(auth_client, project):
    url = reverse("projects:edit_project", kwargs={"pk": project.pk})
    response = auth_client.get(url)
    assert response.status_code == 200


def test_project_update_valid_post_returns_302(
    user, auth_client, project_factory, project_form_data
):
    project = project_factory(owner=user)
    url = reverse("projects:edit_project", kwargs={"pk": project.pk})
    response = auth_client.post(url, data=project_form_data)
    expected_url = reverse("projects:project_detail", kwargs={"pk": project.pk})
    assertRedirects(response, expected_url)


def test_project_update_invalid_post_returns_200(user, auth_client, project_factory):
    project = project_factory(owner=user)
    url = reverse("projects:edit_project", kwargs={"pk": project.pk})
    response = auth_client.post(url, data={"github_url": "foo"})
    assert response.status_code == 200


def test_project_update_redirects_non_owner(auth_client, project_factory):
    project = project_factory()
    url = reverse("projects:edit_project", kwargs={"pk": project.pk})
    response = auth_client.post(url, data={"name": "foo"})
    expected_url = reverse("projects:project_detail", kwargs={"pk": project.pk})
    assertRedirects(response, expected_url)


# FavoritesListView


def test_favorites_requires_login(client):
    url = reverse("projects:favorites")
    response = client.get(url)
    assert response.status_code == 302


def test_favorites_returns_200(auth_client):
    url = reverse("projects:favorites")
    response = auth_client.get(url)
    assert response.status_code == 200
