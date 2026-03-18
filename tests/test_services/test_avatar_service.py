from typing import cast

import pytest
from django.core.files.base import ContentFile

from core.services.avatar import AvatarService


@pytest.fixture
def avatar_service():
    return AvatarService()


def _get_file_size_mb(content_file: ContentFile) -> float:
    """Returns the size of a ContentFile in megabytes."""
    return len(content_file.read()) / 1024 / 1024


def test_generate_avatar_returns_content_file(avatar_service):
    result = avatar_service.generate_avatar(label="test@mail.com")
    assert isinstance(result, ContentFile)
    file_name = cast(str, result.name)
    assert file_name.startswith(avatar_service.gen_prefix)
    assert "test" in file_name
    assert "_avatar." in file_name


def test_generate_avatar_filename_is_unique(avatar_service):
    result1 = avatar_service.generate_avatar(label="test@mail.com")
    result2 = avatar_service.generate_avatar(label="test@mail.com")
    assert result1.name != result2.name


def test_check_size_within_limit(avatar_service):
    class FakeImage:
        size = 100

    assert avatar_service.check_size(FakeImage())


def test_check_size_exceeds_limit(avatar_service):
    class FakeImage:
        size = 999999999

    assert not avatar_service.check_size(FakeImage())


def test_generate_avatar_falls_back_to_webp_if_png_too_large(avatar_service):
    png_size_mb = _get_file_size_mb(
        avatar_service.generate_avatar(label="test@mail.com", mode="PNG")
    )
    webp_size_mb = _get_file_size_mb(
        avatar_service.generate_avatar(label="test@mail.com", mode="WEBP")
    )
    # set limit between PNG and WEBP sizes to trigger WEBP fallback
    avatar_service.config = avatar_service.config.model_copy(
        update={"max_size_mb": (png_size_mb + webp_size_mb) / 2}
    )
    result = avatar_service.generate_avatar(label="test@mail.com")
    assert result.name.endswith(".webp")


def test_generate_avatar_falls_back_to_default_avatar(avatar_service):
    webp_size_mb = _get_file_size_mb(
        avatar_service.generate_avatar(label="test@mail.com", mode="WEBP")
    )
    # set limit well below WEBP size to trigger default avatar fallback
    avatar_service.config = avatar_service.config.model_copy(
        update={"max_size_mb": webp_size_mb * 0.1}
    )
    result = avatar_service.generate_avatar(label="test@mail.com")
    assert result.name == "default_avatar.png"


def test_generate_avatar_falls_back_to_gray_placeholder_if_default_missing(
    avatar_service, tmp_path
):
    webp_size_mb = _get_file_size_mb(
        avatar_service.generate_avatar(label="test@mail.com", mode="WEBP")
    )
    # create file to pass FilePath validation, then delete to simulate missing file
    missing_path = tmp_path / "nonexistent.png"
    missing_path.write_bytes(b"")
    avatar_service.config = avatar_service.config.model_copy(
        update={"max_size_mb": webp_size_mb * 0.1, "default_avatar_path": missing_path}
    )
    missing_path.unlink()
    result = avatar_service.generate_avatar(label="test@mail.com")
    assert result.name == "fallback.png"
