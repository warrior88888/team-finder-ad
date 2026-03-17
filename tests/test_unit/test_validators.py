import pytest

from core.validators import (
    check_email_unique,
    check_github_url,
    normalize_and_check_phone,
)

pytestmark = pytest.mark.django_db


def test_email_is_unique_when_no_users():
    assert check_email_unique("new@mail.com") is True


def test_email_is_not_unique_when_exists(user):
    assert check_email_unique(user.email) is False


def test_email_uniqueness_is_case_insensitive(user):
    assert check_email_unique(user.email.upper()) is False


def test_email_unique_excludes_given_user(user):
    assert check_email_unique(user.email, exclude_user_id=user.pk) is True


def test_empty_github_url_is_valid():
    assert check_github_url("") == (True, None)


def test_valid_github_url():
    assert check_github_url("https://github.com/user") == (True, None)


def test_not_github_domain():
    assert check_github_url("https://gitlab.com/user") == (False, "not_github")


def test_github_url_without_protocol():
    assert check_github_url("http://github.com/user") == (False, "no_protocol")


def test_invalid_phone_format():
    _, is_valid, _ = normalize_and_check_phone("12345")
    assert is_valid is False


def test_normalizes_phone_starting_with_8():
    normalized, is_valid, _ = normalize_and_check_phone("89991234567")
    assert is_valid is True
    assert normalized == "+79991234567"


def test_phone_is_unique_when_no_users():
    _, _, is_unique = normalize_and_check_phone("+79991234567")
    assert is_unique is True


def test_phone_is_not_unique_when_exists(user_factory):
    user_factory(phone="+79991234567")
    _, _, is_unique = normalize_and_check_phone(
        "+79991234567",
        exclude_user_id=0,
    )
    assert is_unique is False


def test_phone_unique_excludes_given_user(user_factory):
    user = user_factory(phone="+79991234567")
    _, _, is_unique = normalize_and_check_phone(
        "+79991234567",
        exclude_user_id=user.pk,
    )
    assert is_unique is True
