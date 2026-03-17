from typing import cast

from core.services.redis import RedisPrefix, redis_client, redis_safe

from .limits import RATE_LIMIT, WINDOW


def build_key(*args: str | int) -> str:
    return RedisPrefix.THROTTLE.key(*args)


@redis_safe(default=None)
def remove_throttled(key: str) -> None:
    redis_client.delete(key)


@redis_safe(default=0)
def set_throttled(key: str, window: int = WINDOW) -> int:
    count = cast(int, redis_client.incr(key))
    if count == 1:
        # First increment — set expiry. Avoids overwriting TTL on subsequent calls.
        redis_client.expire(key, window)
    return count


@redis_safe(default=False)
def exceed_limit(key: str, rate_limit: int = RATE_LIMIT) -> bool:
    count = cast(bytes | None, redis_client.get(key))
    if count:
        return int(count) > rate_limit
    return False


def is_throttled(
    key: str,
    rate_limit: int = RATE_LIMIT,
    window: int = WINDOW,
) -> bool:
    count = set_throttled(key, window)
    return count > rate_limit
