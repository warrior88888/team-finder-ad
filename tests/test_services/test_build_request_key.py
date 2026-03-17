from unittest import mock

import pytest

from core.services.redis import ThrottleAction
from core.services.throttling.request import build_request_key
from core.utils import get_client_ip

pytestmark = pytest.mark.django_db

ACTION = ThrottleAction.LOGIN_FAIL


def test_builds_key_for_authenticated_user(user, request_builder):
    request = request_builder(user=user)
    key = build_request_key(request, action=ACTION)
    assert key is not None
    assert str(user.pk) in key
    assert ACTION in key


def test_builds_key_for_anonymous_user(request_builder):
    request = request_builder()
    key = build_request_key(request, action=ACTION)
    assert key is not None
    assert get_client_ip(request) in key


def test_returns_none_if_no_ip_and_anonymous(request_builder):
    request = request_builder()
    with mock.patch(
        "core.services.throttling.request.get_client_ip",
        return_value="",
    ):
        key = build_request_key(request)
    assert key is None


def test_builds_key_without_action(user, request_builder):
    request = request_builder(user=user)
    key = build_request_key(request)
    assert key is not None
    assert str(user.pk) in key
