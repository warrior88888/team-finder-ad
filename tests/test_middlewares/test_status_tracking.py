from unittest import mock

import pytest

from core.middlewares.status_tracking import OnlineStatusTrackingMiddleware

pytestmark = pytest.mark.django_db


@pytest.fixture
def middleware():
    return OnlineStatusTrackingMiddleware(get_response=lambda r: None)


def test_marks_authenticated_user_online(middleware, user, request_builder):
    request = request_builder(user=user)
    with mock.patch(
        "core.middlewares.status_tracking.user_tracker.mark_online",
    ) as m:
        middleware(request)
        m.assert_called_once_with(user)


def test_marks_anonymous_visitor(middleware, request_builder):
    request = request_builder()
    with mock.patch(
        "core.middlewares.status_tracking.anonymous_tracker.mark_visitor"
    ) as m:
        middleware(request)
        m.assert_called_once()
