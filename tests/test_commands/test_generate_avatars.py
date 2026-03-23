from io import StringIO
from unittest.mock import MagicMock, patch

import pytest
from django.core.management import call_command

pytestmark = pytest.mark.django_db


@pytest.fixture
def mock_users(user_factory):
    return [user_factory(avatar=""), user_factory(avatar="")]


def test_generate_avatars_blank_flag(mock_users):
    out = StringIO()
    err = StringIO()
    for user in mock_users:
        user.save = MagicMock()
    with (
        patch(
            "users.management.commands.generate_avatars.UserSelector"
        ) as mock_selector_cls,
        patch(
            "users.management.commands.generate_avatars.AvatarService"
        ) as mock_service_cls,
    ):
        mock_selector = mock_selector_cls.return_value
        mock_selector.get_users_by_avatar.return_value = mock_users

        mock_service = mock_service_cls.return_value
        mock_service.generate_avatar.return_value = MagicMock(name="avatar.png")
        call_command("generate_avatars", blank=True, stdout=out, stderr=err)
    output = out.getvalue()
    assert "2" in output
    assert mock_service.generate_avatar.call_count == 2
    mock_selector.get_users_by_avatar.assert_called_once_with(
        blank=True, default=False, fallback=False
    )


def test_generate_avatars_handles_exception(mock_users):
    err = StringIO()
    out = StringIO()
    with (
        patch(
            "users.management.commands.generate_avatars.UserSelector"
        ) as mock_selector_cls,
        patch(
            "users.management.commands.generate_avatars.AvatarService"
        ) as mock_service_cls,
    ):
        mock_selector = mock_selector_cls.return_value
        mock_selector.get_users_by_avatar.return_value = mock_users

        mock_service = mock_service_cls.return_value
        mock_service.generate_avatar.side_effect = Exception("generation failed")

        call_command("generate_avatars", blank=True, stdout=out, stderr=err)
    assert "generation failed" in err.getvalue()
    assert "0" in out.getvalue()


def test_generate_avatars_no_users():
    out = StringIO()
    with (
        patch(
            "users.management.commands.generate_avatars.UserSelector"
        ) as mock_selector_cls,
        patch("users.management.commands.generate_avatars.AvatarService"),
    ):
        mock_selector = mock_selector_cls.return_value
        mock_selector.get_users_by_avatar.return_value = []
        call_command("generate_avatars", blank=True, stdout=out)
    assert "0" in out.getvalue()


def test_generate_avatars_default_flag(mock_users):
    for user in mock_users:
        user.save = MagicMock()
    with (
        patch(
            "users.management.commands.generate_avatars.UserSelector"
        ) as mock_selector_cls,
        patch(
            "users.management.commands.generate_avatars.AvatarService"
        ) as mock_service_cls,
    ):
        mock_selector = mock_selector_cls.return_value
        mock_selector.get_users_by_avatar.return_value = mock_users
        mock_service_cls.return_value.generate_avatar.return_value = MagicMock()
        call_command("generate_avatars", default=True, stdout=StringIO())
    mock_selector.get_users_by_avatar.assert_called_once_with(
        blank=False, default=True, fallback=False
    )


def test_generate_avatars_fallback_flag(mock_users):
    for user in mock_users:
        user.save = MagicMock()
    with (
        patch(
            "users.management.commands.generate_avatars.UserSelector"
        ) as mock_selector_cls,
        patch(
            "users.management.commands.generate_avatars.AvatarService"
        ) as mock_service_cls,
    ):
        mock_selector = mock_selector_cls.return_value
        mock_selector.get_users_by_avatar.return_value = mock_users
        mock_service_cls.return_value.generate_avatar.return_value = MagicMock()
        call_command("generate_avatars", fallback=True, stdout=StringIO())
    mock_selector.get_users_by_avatar.assert_called_once_with(
        blank=False, default=False, fallback=True
    )
