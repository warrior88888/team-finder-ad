from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

from core.services.activity_tracking import user_tracker

from .base import BaseMiddleware

if TYPE_CHECKING:
    from django.http import HttpRequest

    from users.types import UserRequest


class ActiveUserMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated and not request.user.is_active:
            request = cast("UserRequest", request)
            user_tracker.remove_online(request.user)
            logout(request)
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
