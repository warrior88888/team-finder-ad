from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.conf import settings

from .get_ip import get_client_ip

if TYPE_CHECKING:
    from django.http import HttpRequest

    from users.types import UserRequest


SKIP_PATHS = getattr(settings, "SERVICES_SKIP_PATHS", [])
SKIP_IPS = getattr(settings, "SERVICES_SKIP_IPS", [])
SKIP_IPS_PREFIXES = getattr(settings, "SERVICES_SKIP_IP_PREFIXES", [])


def should_skip(request: HttpRequest, skip_staff: bool = True) -> bool:
    """Returns True if the request should bypass processing.

    Skips if path, IP, or IP prefix is in the configured exclusion lists,
    or if the user is staff.
    """
    if any(request.path.startswith(p) for p in SKIP_PATHS):
        return True
    ip = get_client_ip(request)
    if ip in SKIP_IPS or any(
        ip.startswith(ip_prefix) for ip_prefix in SKIP_IPS_PREFIXES
    ):
        return True
    if request.user.is_authenticated and skip_staff:
        return cast("UserRequest", request).user.is_staff
    return False
