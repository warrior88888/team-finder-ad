import pytest
from django.http import Http404

from projects.selectors import ProjectSelector

pytestmark = pytest.mark.django_db


@pytest.fixture
def selector():
    return ProjectSelector()


def test_list_projects_returns_all(selector, project, project_factory):
    another_project = project_factory()
    qs = selector.list_projects()
    assert project in qs
    assert another_project in qs


def test_list_projects_annotates_is_favorite_false_for_anonymous(
    selector, project_factory
):
    for _ in range(2):
        project_factory()
    qs = selector.list_projects()
    assert all(pr.is_favorite is False for pr in qs)


def test_list_projects_annotates_is_favorite_true_for_favorited(
    selector, user, project_factory
):
    project = project_factory()
    user.favorites.add(project)
    qs = selector.list_projects(user=user)
    result = next(p for p in qs if p.pk == project.pk)
    assert result.is_favorite is True


def test_list_projects_annotates_is_favorite_false_for_non_favorited(
    selector, user, project_factory
):
    project = project_factory()
    qs = selector.list_projects(user=user)
    result = next(p for p in qs if p.pk == project.pk)
    assert result.is_favorite is False


def test_list_projects_favorites_only_excludes_non_favorited(
    selector, user, project_factory
):
    favorited = project_factory()
    not_favorited = project_factory()
    user.favorites.add(favorited)
    qs = selector.list_projects(user=user, favorites_only=True)
    assert favorited in qs
    assert not_favorited not in qs


def test_list_projects_favorites_only_annotates_is_favorite_true(
    selector, user, project_factory
):
    project = project_factory()
    user.favorites.add(project)
    qs = selector.list_projects(user=user, favorites_only=True)
    result = next(p for p in qs if p.pk == project.pk)
    assert result.is_favorite is True  # type: ignore[UnresolvedAttribute]


def test_list_projects_favorites_only_ignored_for_anonymous(selector, project_factory):
    project_factory()
    qs = selector.list_projects(favorites_only=True)
    assert all(p.is_favorite is False for p in qs)  # type: ignore[UnresolvedAttribute]


def test_project_detail_returns_project(selector, project):
    result = selector.project_detail(project_pk=project.pk)
    assert result.pk == project.pk


def test_project_detail_raises_404_if_not_found(selector):
    with pytest.raises(Http404):
        selector.project_detail(project_pk=99999)


def test_project_detail_with_participants_annotates_count(
    selector, project, user_factory
):
    project.participants.add(user_factory())
    result = selector.project_detail(project_pk=project.pk, with_participants=True)
    assert result.participants_count >= 1  # type: ignore[UnresolvedAttribute]
