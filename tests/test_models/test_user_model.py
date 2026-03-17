from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_avatar_generated_on_create(user, settings):
    assert user.avatar
    assert user.avatar.name.startswith("avatars/av_serv_gen_")
    assert Path(settings.MEDIA_ROOT / user.avatar.name).exists()


@pytest.mark.django_db
def test_avatar_not_regenerated_on_save_if_file_exists(user):
    original_name = user.avatar.name
    user.name = "foo"
    user.save()
    assert user.avatar.name == original_name


def test_avatar_regenerated_if_file_missing(user, settings):
    Path(settings.MEDIA_ROOT / user.avatar.name).unlink()
    user.save()
    assert Path(settings.MEDIA_ROOT / user.avatar.name).exists()


def test_old_avatar_deleted_on_new_upload(user, settings):
    old_avatar_path = Path(settings.MEDIA_ROOT / user.avatar.name)
    assert old_avatar_path.exists()

    new_file = SimpleUploadedFile(
        "new.png", b"fakeimagecontent", content_type="image/png"
    )
    user.avatar = new_file
    user.save()
    assert not old_avatar_path.exists()


def test_new_avatar_saved_after_upload(user, settings):
    new_file = SimpleUploadedFile(
        "new.png", b"fakeimagecontent", content_type="image/png"
    )
    user.avatar = new_file
    user.save()
    assert "new" in cast(str, user.avatar.name)
    assert Path(settings.MEDIA_ROOT / user.avatar.name).exists()


def test_old_avatar_not_deleted_on_simple_save(user, settings):
    old_avatar_path = Path(settings.MEDIA_ROOT / user.avatar.name)
    user.about = "Обновлённое описание"
    user.save()
    assert old_avatar_path.exists()


def test_no_double_avatar_generation_on_create(user_factory):
    with patch(
        "users.models.models._avatar_service.generate_avatar",
        wraps=lambda **kwargs: None,
    ) as mock:
        user_factory()
    assert mock.call_count == 1
