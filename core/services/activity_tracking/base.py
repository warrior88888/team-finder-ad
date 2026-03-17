from abc import ABC

from core.services.redis import RedisPrefix, redis_client, redis_safe


class BaseTracker(ABC):
    """Abstract base for Redis-backed activity trackers.

    Subclasses must define PREFIX (RedisPrefix) and optionally TTL (default 120s).
    """

    TTL: int = 120
    PREFIX: RedisPrefix

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "PREFIX"):
            raise TypeError(f"{cls.__name__} must define PREFIX")

    @classmethod
    @redis_safe(default=None)
    def _set(cls, identifier: str | int) -> None:
        # TOUCH resets TTL without overwriting the value
        key = cls.PREFIX.key(identifier)
        if redis_client.exists(key):
            redis_client.touch(key)
        else:
            redis_client.set(key, "1", ex=cls.TTL)

    @classmethod
    @redis_safe(default=[])
    def _get_all_ids(cls) -> list[str]:
        # SCAN instead of KEYS — avoids blocking Redis on large datasets
        return [
            cls.PREFIX.extract_id(key)
            for key in redis_client.scan_iter(
                match=cls.PREFIX.pattern(),
                count=1000,
            )
        ]

    @classmethod
    @redis_safe(default=None)
    def _remove(cls, identifier: str | int) -> None:
        redis_client.delete(cls.PREFIX.key(identifier))

    @classmethod
    @redis_safe(default=0)
    def get_count(cls) -> int:
        # SCAN doesn't load all keys to memory
        return sum(
            1
            for _ in redis_client.scan_iter(
                match=cls.PREFIX.pattern(),
                count=1000,
            )
        )

    @classmethod
    @redis_safe(default=False)
    def is_active(cls, identifier: str | int) -> bool:
        return bool(redis_client.exists(cls.PREFIX.key(identifier)))
