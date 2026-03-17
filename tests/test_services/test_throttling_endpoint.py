from collections.abc import Callable

import pytest
from django.http import HttpRequest, HttpResponse, JsonResponse

from core.services.redis import ThrottleAction
from core.services.throttling.endpoint import throttle_endpoint

pytestmark = pytest.mark.django_db

ACTION = ThrottleAction.AVATAR_RESET


def dummy_view(request, *args, **kwargs):
    return JsonResponse({"status": "ok"})


@pytest.fixture
def decorated_view() -> Callable[[HttpRequest], HttpResponse]:
    return throttle_endpoint(action=ACTION, rate_limit=3)(dummy_view)


def test_allows_request_below_limit(decorated_view, request_builder, user):
    request = request_builder(user=user)
    response = decorated_view(request)
    assert response.status_code == 200


def test_returns_429_when_limit_exceeded(decorated_view, request_builder, user):
    request = request_builder(user=user)
    responses = [decorated_view(request) for _ in range(4)]
    assert responses[-1].status_code == 429
