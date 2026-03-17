from typing import cast
from unittest import mock

import pytest

from core.middlewares.check_active import ActiveUserMiddleware
from users.types import UserRequest

pytestmark = pytest.mark.django_db


@pytest.fixture
def middleware():
    return ActiveUserMiddleware(get_response=lambda r: None)


def test_active_user_passes_through(middleware, user, request_builder):
    request = cast("UserRequest", request_builder(user=user))
    response = middleware(request)
    assert response is None


def test_inactive_user_is_logged_out(middleware, user, request_builder):
    user.is_active = False
    user.save()
    request = cast("UserRequest", request_builder(user=user))
    with mock.patch(
        "core.middlewares.check_active.user_tracker.remove_online",
    ) as m:
        response = middleware(request)
        m.assert_called_once_with(user)
    assert response.status_code == 302


def test_anonymous_user_passes_through(middleware, request_builder):
    request = request_builder()
    response = middleware(request)
    assert response is None
