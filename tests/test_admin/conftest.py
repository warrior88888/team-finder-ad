import pytest
from django.contrib.auth.models import Group
from django.contrib.messages.storage.fallback import FallbackStorage

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user(user_factory):
    return user_factory(is_staff=True, is_superuser=True)


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def admin_request(request_builder, admin_user):
    request = request_builder(user=admin_user)
    request._messages = FallbackStorage(request)
    return request


@pytest.fixture
def group():
    return Group.objects.create(name="Test Group")
