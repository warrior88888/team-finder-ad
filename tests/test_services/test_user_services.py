from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

from core.services.activity_tracking import user_tracker
from core.services.avatar import AvatarService
from users import services
from users.forms import UserEditForm, UserRegisterForm

if TYPE_CHECKING:
    from users.models import User as UserModel
    from users.types import UserRequest

pytestmark = pytest.mark.django_db


def test_register_user(request_builder, user_factory, user_register_form_data):
    request = request_builder(
        viewname="users:register",
        method="POST",
        data=user_register_form_data,
    )
    returned_user: UserModel = services.register_user(
        request=request, form=UserRegisterForm(data=user_register_form_data)
    )
    assert user_factory._meta.model.objects.count() == 1
    assert returned_user.email == user_register_form_data["email"]
    assert returned_user.check_password(user_register_form_data["password"])


def test_login_user(user, password, request_builder):
    request = request_builder(
        viewname="users:register",
        method="POST",
    )
    returned_user = services.login_user(
        request=request,
        email=user.email,
        password=password,
    )
    assert returned_user == user


def test_login_user_invalid_password(user, fake_password, request_builder):
    request = request_builder(
        viewname="users:register",
        method="POST",
    )
    with pytest.raises(ValidationError):
        services.login_user(request=request, email=user.email, password=fake_password)


def test_edit_user(user, user_profile_form_data, request_builder):
    form = UserEditForm(data=user_profile_form_data, instance=user)
    request = cast(
        "UserRequest",
        request_builder(
            viewname="users:edit_profile",
            user=user,
            method="POST",
        ),
    )
    returned_user = services.edit_profile(
        request=request,
        form=form,
    )
    user.refresh_from_db()
    assert returned_user.pk == user.pk
    assert returned_user.about == user_profile_form_data["about"]


def test_logout_user(user, request_builder):
    request = cast("UserRequest", request_builder(user=user))
    user_tracker.mark_online(user)
    services.logout_user(request)
    assert not user_tracker.is_online(user)


def test_logout_unauthenticated_user_does_nothing(request_builder):
    request = request_builder()
    # Logout attempt for anon attempt must not raise any exceptions
    services.logout_user(cast("UserRequest", request))


def test_change_password(user, request_builder):
    new_password = "newP@ssw0rd123"
    request = cast("UserRequest", request_builder(user=user))
    form = PasswordChangeForm(
        user=user,
        data={
            "old_password": "x*bR%N72:5",
            "new_password1": new_password,
            "new_password2": new_password,
        },
    )
    assert form.is_valid()
    services.change_password(request=request, form=form)
    user.refresh_from_db()
    assert user.check_password(new_password)


def test_reset_avatar_generates_new_avatar(user, request_builder):
    request = cast("UserRequest", request_builder(user=user))
    new_avatar_url = services.reset_avatar(request=request)
    user.refresh_from_db()
    assert new_avatar_url == user.avatar.url
    assert AvatarService.file_exists(user.avatar)
