from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from django.conf import settings
from faker import Faker
from pytest_factoryboy import register

from core.services.redis import redis_client
from tests.factories import ProjectFactory, UserFactory
from tests.utils.builders import RequestBuilder

if TYPE_CHECKING:
    from collections.abc import Iterator

    from redis import Redis

# Factory registration


register(UserFactory)
register(ProjectFactory)


# Session-scoped teardown


@pytest.fixture(scope="session", autouse=True)
def cleanup_media_after_tests() -> Iterator[None]:
    yield
    if Path(settings.MEDIA_ROOT).exists():
        shutil.rmtree(settings.MEDIA_ROOT)


@pytest.fixture(autouse=True)
def clean_up_redis_after_tests() -> Iterator[None]:
    yield
    redis_client.flushdb()


# Infrastructure


@pytest.fixture
def redis_test_client() -> Redis:
    return redis_client


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def request_builder() -> RequestBuilder:
    return RequestBuilder()


@pytest.fixture
def auth_client(user, client):
    client.force_login(user)
    return client


# Auth data


@pytest.fixture
def password() -> str:
    return "x*bR%N72:5"


@pytest.fixture
def fake_password(faker) -> str:
    return faker.password(length=10)


# Form data


@pytest.fixture
def user_register_form_data() -> dict[str, str]:
    return {
        "name": "name",
        "surname": "surname",
        "email": "email@example.com",
        "password": "iuhEF24YHF8723YF287F",
    }


@pytest.fixture
def user_profile_form_data() -> dict[str, str]:
    return {
        "name": "name",
        "surname": "surname",
        "about": "about",
        "phone": "+79999999999",
        "github_url": "https://github.com/test/",
    }


@pytest.fixture
def project_form_data() -> dict[str, str]:
    return {
        "name": "name",
        "description": "description",
        "github_url": "https://github.com/test/",
        "status": "open",
    }
