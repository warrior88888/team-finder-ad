import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_user_changelist_accessible(admin_client):
    response = admin_client.get(reverse("admin:users_user_changelist"))
    assert response.status_code == 200


def test_user_add_accessible(admin_client):
    response = admin_client.get(reverse("admin:users_user_add"))
    assert response.status_code == 200


def test_user_change_accessible(admin_client, user):
    response = admin_client.get(reverse("admin:users_user_change", args=[user.pk]))
    assert response.status_code == 200


def test_user_changelist_not_accessible_for_anonymous(client):
    response = client.get(reverse("admin:users_user_changelist"))
    assert response.status_code == 302


def test_user_changelist_not_accessible_for_regular_user(client, user):
    client.force_login(user)
    response = client.get(reverse("admin:users_user_changelist"))
    assert response.status_code == 302


def test_project_changelist_accessible(admin_client):
    response = admin_client.get(reverse("admin:projects_project_changelist"))
    assert response.status_code == 200


def test_project_add_accessible(admin_client):
    response = admin_client.get(reverse("admin:projects_project_add"))
    assert response.status_code == 200


def test_project_change_accessible(admin_client, project):
    response = admin_client.get(
        reverse("admin:projects_project_change", args=[project.pk])
    )
    assert response.status_code == 200


def test_project_changelist_not_accessible_for_anonymous(client):
    response = client.get(reverse("admin:projects_project_changelist"))
    assert response.status_code == 302


def test_project_changelist_not_accessible_for_regular_user(client, user):
    client.force_login(user)
    response = client.get(reverse("admin:projects_project_changelist"))
    assert response.status_code == 302


def test_group_changelist_accessible(admin_client):
    response = admin_client.get(reverse("admin:auth_group_changelist"))
    assert response.status_code == 200


def test_group_add_accessible(admin_client):
    response = admin_client.get(reverse("admin:auth_group_add"))
    assert response.status_code == 200


def test_group_change_accessible(admin_client, group):
    response = admin_client.get(reverse("admin:auth_group_change", args=[group.pk]))
    assert response.status_code == 200


def test_group_changelist_not_accessible_for_anonymous(client):
    response = client.get(reverse("admin:auth_group_changelist"))
    assert response.status_code == 302


def test_group_changelist_not_accessible_for_regular_user(client, user):
    client.force_login(user)
    response = client.get(reverse("admin:auth_group_changelist"))
    assert response.status_code == 302
