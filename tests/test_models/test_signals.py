from pathlib import Path

import pytest

pytestmark = pytest.mark.django_db


def test_avatar_file_deleted_on_user_delete(user, settings):
    avatar_path = Path(settings.MEDIA_ROOT) / user.avatar.name
    assert avatar_path.exists()
    user.delete()
    assert not avatar_path.exists()


def test_avatar_file_deleted_on_queryset_delete(user, settings):
    avatar_path = Path(settings.MEDIA_ROOT) / user.avatar.name
    assert avatar_path.exists()
    type(user).objects.filter(pk=user.pk).delete()
    assert not avatar_path.exists()


def test_multiple_users_avatars_deleted_on_queryset_delete(
    user, user_factory, settings
):
    users = user_factory.create_batch(3)
    avatar_paths = [Path(settings.MEDIA_ROOT) / u.avatar.name for u in users]
    assert all(p.exists() for p in avatar_paths)
    type(user).objects.filter(pk__in=[u.pk for u in users]).delete()
    assert all(not p.exists() for p in avatar_paths)


def test_no_error_if_avatar_is_empty(user):
    user.avatar = None
    user.save()
    try:
        user.delete()
    except Exception as e:
        pytest.fail(f"delete() raised unexpectedly: {e}")


def test_no_error_if_file_already_missing(user_factory, settings):
    user = user_factory()
    avatar_path = Path(settings.MEDIA_ROOT) / user.avatar.name
    avatar_path.unlink()
    try:
        user.delete()
    except Exception as e:
        pytest.fail(f"delete() raised unexpectedly: {e}")


def test_user_deleted_from_db(user):
    pk = user.pk
    user.delete()
    assert not type(user).objects.filter(pk=pk).exists()
