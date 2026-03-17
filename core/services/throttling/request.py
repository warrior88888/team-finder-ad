from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.utils import get_client_ip

from .throttling import build_key

if TYPE_CHECKING:
    from django.http import HttpRequest

    from core.services.redis import ThrottleAction

logger = logging.getLogger(__name__)


def build_request_key(
    request: HttpRequest, action: ThrottleAction | None = None
) -> str | None:
    """Builds a throttle key scoped to user ID (authenticated) or IP (anonymous).

    Returns None if the request is anonymous and IP cannot be determined.
    """
    parts = []
    if action:
        parts.append(action)
    if request.user.is_authenticated:
        parts.append(str(request.user.pk))
        return build_key(*parts)
    ip = get_client_ip(request)
    if not ip:
        return None
    parts.append(ip)
    return build_key(*parts)
