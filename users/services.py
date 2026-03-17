from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.core.exceptions import ValidationError
from django.db import transaction

from core.services.activity_tracking import user_tracker
from core.services.throttling.login import (
    check_login_attempts,
    record_login_failure,
    reset_login_attempts,
)
from core.utils import get_client_ip

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.contrib.auth.forms import PasswordChangeForm
    from django.http import HttpRequest

    from users.forms import UserEditForm, UserRegisterForm
    from users.models import User as UserModel
    from users.types import UserRequest


logger = logging.getLogger(__name__)


def register_user(*, request: HttpRequest, form: UserRegisterForm) -> UserModel:
    user = form.save()
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    logger.info("User created and authenticated: pk=%s", user.pk)
    return user


def login_user(*, request: HttpRequest, email: str, password: str) -> AbstractBaseUser:
    ip = get_client_ip(request)
    check_login_attempts(email, ip)
    user = authenticate(request, username=email, password=password)
    if user is None:
        record_login_failure(email, ip)
        raise ValidationError("Неверный логин или пароль")
    reset_login_attempts(email, ip)
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    logger.info("User logged in successfully: pk=%s", user.pk)
    return user


def edit_profile(*, request: UserRequest, form: UserEditForm) -> UserModel:
    form.instance = request.user
    form.save()
    logger.info("Profile edited successfully: pk=%s", request.user.pk)
    return request.user


def logout_user(request: UserRequest) -> None:
    """Logs out the user and removes online status. Skip if not authenticated."""
    if not request.user.is_authenticated:
        logger.debug("Logout attempt by unauthenticated user")
        return
    user_tracker.remove_online(request.user)
    logger.info("User logged out: pk=%s", request.user.pk)
    logout(request)


def change_password(*, request: UserRequest, form: PasswordChangeForm) -> UserModel:
    """Changes password and updates session to prevent logout."""
    user: UserModel = form.save()
    update_session_auth_hash(request, user)
    logger.info("Password changed successfully: pk=%s", user.pk)
    return user


@transaction.atomic
def reset_avatar(*, request: UserRequest) -> str:
    """Deletes current avatar file, clears the field,
    and returns the new generated avatar URL."""
    user = request.user
    old_avatar = user.avatar.name
    avatar = user.avatar
    avatar.delete(save=False)  # type: ignore[reportAttributeAccessIssue]
    user.avatar = None
    user.save(update_fields=["avatar"])
    user.refresh_from_db(fields=["avatar"])
    logger.info(
        "Avatar reset: pk=%s old=%s new=%s",
        user.pk,
        old_avatar,
        user.avatar.name,  # type: ignore[reportAttributeAccessIssue]
    )
    return user.avatar.url  # type: ignore[reportAttributeAccessIssue]
