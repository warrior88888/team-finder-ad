import pytest
from django.http import Http404

from users.selectors import UserSelector

pytestmark = pytest.mark.django_db


@pytest.fixture
def selector():
    return UserSelector()


def test_participants_list_returns_all_users(selector, user, user_factory):
    another_user = user_factory()
    qs = selector.participants_list()
    assert user in qs
    assert another_user in qs


def test_participants_list_filters_by_favorite_project_owners(
    selector, user, user_factory, project_factory
):
    owner = user_factory()
    project = project_factory(owner=owner)
    user.favorites.add(project)
    qs = selector.participants_list(filter_by="owners-of-favorite-projects", user=user)
    assert owner in qs
    assert user not in qs


def test_participants_list_ignores_filter_if_no_user(selector, user_factory):
    qs = selector.participants_list(filter_by="owners-of-favorite-projects", user=None)
    assert qs.count() == user_factory._meta.model.objects.count()


def test_participants_list_ignores_unknown_filter(selector, user):
    qs = selector.participants_list(filter_by="unknown-filter", user=user)
    assert user in qs


def test_user_details_returns_user(selector, user):
    result = selector.user_details(user_pk=user.pk)
    assert result.pk == user.pk


def test_user_details_raises_404_for_missing_user(selector):
    with pytest.raises(Http404):
        selector.user_details(user_pk=99999)


def test_get_users_by_avatar_raises_if_no_filters(selector):
    with pytest.raises(ValueError):  # noqa: PT011
        selector.get_users_by_avatar()


def test_get_users_by_avatar_blank(selector, user):
    type(user).objects.filter(pk=user.pk).update(avatar="")
    user.refresh_from_db()
    qs = selector.get_users_by_avatar(blank=True)
    assert user in qs


def test_get_users_by_avatar_generated(selector, user):
    qs = selector.get_users_by_avatar(generated=True)
    assert user in qs


def test_get_users_by_avatar_filters_by_user_ids(selector, user, user_factory):
    another_user = user_factory()
    qs = selector.get_users_by_avatar(generated=True, user_ids=[user.pk])
    assert user in qs
    assert another_user not in qs
