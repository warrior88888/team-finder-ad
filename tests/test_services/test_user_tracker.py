import pytest

from core.services.activity_tracking import user_tracker
from core.services.redis import RedisPrefix

pytestmark = pytest.mark.django_db


def test_mark_online(user, redis_test_client):
    user_tracker.mark_online(user)
    key = RedisPrefix.ONLINE.key(user.pk)
    assert redis_test_client.get(key) == "1"


def test_is_online(user, user_factory):
    another_user = user_factory()
    user_tracker.mark_online(user)
    assert user_tracker.is_online(user)
    assert not user_tracker.is_online(another_user)


def test_remove_online(user):
    user_tracker.mark_online(user)
    user_tracker.remove_online(user)
    assert not user_tracker.is_online(user)


def test_get_online_users_ids(user, user_factory):
    another_user = user_factory()
    user_tracker.mark_online(user)
    user_tracker.mark_online(another_user)
    ids = user_tracker.get_online_users_ids()
    assert set(ids) == {user.pk, another_user.pk}
    user_tracker.remove_online(user)
    user_tracker.remove_online(another_user)
    assert len(user_tracker.get_online_users_ids()) == 0
