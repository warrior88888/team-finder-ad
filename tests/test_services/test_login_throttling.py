import contextlib
from unittest import mock

import pytest
from django.core.exceptions import ValidationError

from core.services.throttling import OverLimitError
from core.services.throttling.login import build_login_key
from core.utils import get_client_ip
from users import services

pytestmark = pytest.mark.django_db


def test_failed_login_increments_counter(
    user, fake_password, redis_test_client, request_builder
):
    request = request_builder(viewname="users:login", method="POST")
    with contextlib.suppress(ValidationError):
        services.login_user(request=request, email=user.email, password=fake_password)
    key = build_login_key(email=user.email, ip=get_client_ip(request))
    assert int(redis_test_client.get(key)) == 1


def test_successful_login_resets_counter(
    user, fake_password, password, redis_test_client, request_builder
):
    request = request_builder(viewname="users:login", method="POST")
    with contextlib.suppress(ValidationError):
        services.login_user(request=request, email=user.email, password=fake_password)
    with contextlib.suppress(ValidationError):
        services.login_user(request=request, email=user.email, password=password)
    key = build_login_key(email=user.email, ip=get_client_ip(request))
    assert not redis_test_client.exists(key)


def test_login_raises_over_limit_error_after_max_attempts(
    user, fake_password, password, redis_test_client, request_builder
):
    request = request_builder(viewname="users:login", method="POST")
    with mock.patch(
        "core.services.throttling.login.LOGIN_FAILS_LIMIT",
        3,
    ):
        for _ in range(4):
            with contextlib.suppress(ValidationError):
                services.login_user(
                    request=request, email=user.email, password=fake_password
                )
        with pytest.raises(OverLimitError):
            services.login_user(request=request, email=user.email, password=password)
