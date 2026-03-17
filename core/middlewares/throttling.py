import logging

from django.http import HttpRequest

from core.services.redis import RedisPrefix
from core.services.throttling import build_request_key, is_throttled
from core.views import error_429

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __call__(self, request: HttpRequest):
        if not self.should_skip(request):
            ip = self.get_client_ip(request)
            key = build_request_key(request)

            if key and is_throttled(key):
                identifier = RedisPrefix.THROTTLE.extract_id(key)
                logger.warning(
                    "Throttling limit exceeded for identifier: %s (IP: %s) on path: %s",
                    identifier,
                    ip,
                    request.path,
                )
                return error_429(request)

        return self.get_response(request)
