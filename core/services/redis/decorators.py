import logging
from functools import wraps
from typing import Any

from redis.exceptions import ConnectionError, RedisError, TimeoutError

logger = logging.getLogger(__name__)


def redis_safe(default: Any = None):
    """Decorator catches Redis errors and returns a default value"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ConnectionError, TimeoutError):
                logger.warning(
                    "Redis connection unavailable in function '%s'",
                    func.__name__,
                    exc_info=True,
                )
                return default
            except RedisError:
                logger.error(
                    "Redis command execution failed in function '%s'",
                    func.__name__,
                    exc_info=True,
                )
                return default

        return wrapper

    return decorator
