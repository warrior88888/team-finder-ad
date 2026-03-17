from unittest import mock

import pytest

from core.middlewares.throttling import ThrottlingMiddleware

pytestmark = pytest.mark.django_db


@pytest.fixture
def middleware():
    return ThrottlingMiddleware(get_response=lambda r: None)


def test_allows_request_below_limit(middleware, user, request_builder):
    request = request_builder(user=user)
    response = middleware(request)
    assert response is None


def test_returns_429_when_limit_exceeded(middleware, user, request_builder):
    request = request_builder(user=user)
    with mock.patch(
        "core.middlewares.throttling.is_throttled",
        return_value=True,
    ):
        response = middleware(request)
    assert response.status_code == 429
