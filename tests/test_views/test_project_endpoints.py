import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


# toggle_favorite


def test_toggle_favorite_requires_login(client, project):
    url = reverse("projects:toggle_favorite", kwargs={"pk": project.pk})
    response = client.post(url)
    assert response.status_code == 302


def test_toggle_favorite_returns_200(auth_client, project):
    url = reverse("projects:toggle_favorite", kwargs={"pk": project.pk})
    response = auth_client.post(url)
    assert response.status_code == 200
    assert "favorited" in response.json()


# toggle_participate


def test_toggle_participate_requires_login(client, project):
    url = reverse("projects:toggle_participate", kwargs={"pk": project.pk})
    response = client.post(url)
    assert response.status_code == 302


def test_toggle_participate_returns_200(auth_client, project_factory):
    project = project_factory()
    url = reverse("projects:toggle_participate", kwargs={"pk": project.pk})
    response = auth_client.post(url)
    assert response.status_code == 200
    assert "participating" in response.json()
    assert "participants_count" in response.json()


# complete_project


def test_complete_project_requires_login(client, project):
    url = reverse("projects:complete_project", kwargs={"pk": project.pk})
    response = client.post(url)
    assert response.status_code == 302


def test_complete_project_returns_200_for_owner(auth_client, user, project_factory):
    project = project_factory(owner=user)
    url = reverse("projects:complete_project", kwargs={"pk": project.pk})
    response = auth_client.post(url)
    assert response.status_code == 200


def test_complete_project_returns_403_for_non_owner(auth_client, project_factory):
    project = project_factory()
    url = reverse("projects:complete_project", kwargs={"pk": project.pk})
    response = auth_client.post(url)
    assert response.status_code == 403


def test_complete_project_returns_400_if_already_closed(
    auth_client, user, project_factory
):
    project = project_factory(owner=user, status="closed")
    url = reverse("projects:complete_project", kwargs={"pk": project.pk})
    response = auth_client.post(url)
    assert response.status_code == 400
