from unittest.mock import patch

import pytest

from users.admin.filters import OnlineStatusFilter

pytestmark = pytest.mark.django_db


@pytest.fixture
def online_filter(request_builder, admin_request, admin_user):
    return OnlineStatusFilter(
        request=admin_request,
        params={},
        model=type(admin_user),
        model_admin=admin_user,
    )


def test_get_online_ids_returns_cached_value(online_filter):
    with patch("users.admin.filters.cache.get", return_value=[1, 2, 3]):
        ids = online_filter._get_online_ids()
    assert ids == [1, 2, 3]


def test_get_online_ids_calls_tracker_on_cache_miss(online_filter):
    with (
        patch("users.admin.filters.cache.get", return_value=None),
        patch("users.admin.filters.cache.set") as mock_set,
        patch(
            "users.admin.filters.user_tracker.get_online_users_ids",
            return_value=[4, 5],
        ) as mock_tracker,
    ):
        ids = online_filter._get_online_ids()
    assert ids == [4, 5]
    mock_tracker.assert_called_once()
    mock_set.assert_called_once_with(
        OnlineStatusFilter.CACHE_KEY, [4, 5], OnlineStatusFilter.CACHE_TTL
    )


def test_queryset_filters_online_users(admin_request, online_filter, user):
    with patch.object(OnlineStatusFilter, "_get_online_ids", return_value=[user.pk]):
        online_filter.used_parameters = {"online": "yes"}
        result = online_filter.queryset(admin_request, type(user).objects.all())
    assert user in result


def test_queryset_excludes_online_users(admin_request, online_filter, user):
    with patch.object(OnlineStatusFilter, "_get_online_ids", return_value=[user.pk]):
        online_filter.used_parameters = {"online": "no"}
        result = online_filter.queryset(admin_request, type(user).objects.all())
    assert user not in result


def test_queryset_returns_all_when_no_filter(admin_request, online_filter, user):
    with patch.object(OnlineStatusFilter, "_get_online_ids", return_value=[]):
        online_filter.used_parameters = {}
        result = online_filter.queryset(admin_request, type(user).objects.all())
    assert user in result
