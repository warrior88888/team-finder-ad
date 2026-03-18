import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model

from core.services.activity_tracking import user_tracker
from users.admin.main import UserAdmin

pytestmark = pytest.mark.django_db

User = get_user_model()


@pytest.fixture
def model_admin():
    return UserAdmin(User, AdminSite())


def test_block_users(model_admin, admin_request, user, user_factory):
    another_user = user_factory()
    queryset = User.objects.filter(pk__in=[user.pk, another_user.pk])
    model_admin.block_users(admin_request, queryset)
    user.refresh_from_db()
    another_user.refresh_from_db()
    assert user.is_active is False
    assert another_user.is_active is False


def test_block_users_remove_online(model_admin, admin_request, user):
    user_tracker.mark_online(user)
    queryset = User.objects.filter(pk=user.pk)
    model_admin.block_users(admin_request, queryset)
    assert user_tracker.is_online(user) is False


def test_unblock_users(model_admin, admin_request, user):
    user.is_active = False
    user.save()
    queryset = User.objects.filter(pk=user.pk)
    model_admin.unblock_users(admin_request, queryset)
    user.refresh_from_db()
    assert user.is_active is True
