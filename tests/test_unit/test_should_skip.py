from unittest import mock

import pytest

from core.utils import should_skip

pytestmark = pytest.mark.django_db


def test_skips_excluded_path(request_builder):
    request = request_builder()
    with mock.patch(
        "core.utils.should_skip.SKIP_PATHS",
        ["/projects/list/"],
    ):
        assert should_skip(request) is True


def test_does_not_skip_normal_path(request_builder):
    request = request_builder()
    assert should_skip(request) is False


def test_skips_excluded_ip(request_builder):
    request = request_builder()
    with mock.patch(
        "core.utils.should_skip.SKIP_IPS",
        ["127.0.0.1"],
    ):
        assert should_skip(request) is True


def test_skips_excluded_ip_prefix(request_builder):
    request = request_builder()
    with mock.patch(
        "core.utils.should_skip.SKIP_IPS_PREFIXES",
        ["127."],
    ):
        assert should_skip(request) is True


def test_skips_staff_user(user, request_builder):
    user.is_staff = True
    user.save()
    request = request_builder(user=user)
    assert should_skip(request) is True


def test_not_skips_staff_with_false_flag(user, request_builder):
    user.is_staff = True
    user.save()
    request = request_builder(user=user)
    assert should_skip(request, skip_staff=False) is False


def test_does_not_skip_regular_user(user, request_builder):
    request = request_builder(user=user)
    assert should_skip(request) is False


def test_does_not_skip_anonymous_user(request_builder):
    request = request_builder()
    assert should_skip(request) is False
