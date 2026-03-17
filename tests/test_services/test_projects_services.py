import pytest
from django.core.exceptions import PermissionDenied

from projects import services
from projects.forms import ProjectForm
from projects.models import Project

pytestmark = pytest.mark.django_db


def test_create_project(user, project_form_data):
    form = ProjectForm(data=project_form_data)
    assert form.is_valid()
    project = services.create_project(user=user, form=form)
    assert Project.objects.count() == 1
    assert project.owner == user
    assert project.participants.filter(pk=user.pk).exists()


def test_toggle_project_favorite(user, project):
    is_favorite = services.toggle_project_favorite(user=user, project=project)
    assert is_favorite
    assert project in user.favorites.all()
    is_favorite = services.toggle_project_favorite(user=user, project=project)
    assert not is_favorite
    assert project not in user.favorites.all()


def test_toggle_participate(user, project_factory):
    another_project = project_factory()
    is_participant, count = services.toggle_project_participate(
        user=user, project=another_project
    )
    assert is_participant
    assert count == 2
    assert user in another_project.participants.all()
    is_participant, count = services.toggle_project_participate(
        user=user, project=another_project
    )
    assert not is_participant
    assert count == 1
    assert user not in another_project.participants.all()


def test_owner_cannot_leave_project(user, project_factory):
    project = project_factory(owner=user)
    is_participant, count = services.toggle_project_participate(
        user=user, project=project
    )
    assert is_participant is True
    assert count == 1
    assert user in project.participants.all()


def test_owner_complete_project(user, project_factory):
    project = project_factory(owner=user)
    status = services.owner_complete_project(user=user, project=project)
    assert status == "closed"
    assert project.status == "closed"


def test_owner_cannot_complete_closed_project(user, project_factory):
    project = project_factory(owner=user, status="closed")
    with pytest.raises(ValueError, match="Project is already closed"):
        services.owner_complete_project(user=user, project=project)
    project.refresh_from_db()
    assert project.status == "closed"


def test_not_owner_cannot_complete_closed_project(user, project_factory):
    another_project = project_factory()
    with pytest.raises(PermissionDenied):
        services.owner_complete_project(user=user, project=another_project)
    another_project.refresh_from_db()
    assert another_project.status == "open"


def test_owner_edit_project(project, project_form_data):
    project_form_data["name"] = "foo"
    form = ProjectForm(data=project_form_data)
    project = services.update_project(project=project, form=form)
    project.refresh_from_db()
    assert project.name == "foo"
