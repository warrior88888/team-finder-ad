from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse

from core.services.redis import RedisPrefix
from core.utils import should_skip

from .request import build_request_key
from .throttling import RATE_LIMIT, WINDOW, is_throttled

if TYPE_CHECKING:
    from django.http import HttpRequest

    from core.services.redis import ThrottleAction

logger = logging.getLogger(__name__)


def throttle_endpoint(
    action: ThrottleAction,
    rate_limit: int = RATE_LIMIT,
    window: int = WINDOW,
):
    """Decorator that rate limits a view by ThrottleAction,
    returning 429 if exceeded."""

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if should_skip(request):
                return view_func(request, *args, **kwargs)
            key = build_request_key(request, action=action)
            if key and is_throttled(key, rate_limit=rate_limit, window=window):
                logger.warning(
                    "Action throttle limit exceeded: action=%s user=%s",
                    action,
                    RedisPrefix.THROTTLE.extract_id_after_action(
                        key=key, action=action
                    ),
                )
                return JsonResponse({"error": "Too many requests"}, status=429)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
