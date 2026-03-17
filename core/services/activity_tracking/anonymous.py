from core.services.redis import RedisPrefix

from .base import BaseTracker


class AnonymousTracker(BaseTracker):
    """Tracks anonymous visitors by IP address."""

    PREFIX = RedisPrefix.ANONYMOUS

    @classmethod
    def mark_visitor(cls, ip_address: str) -> None:
        cls._set(ip_address)

    @classmethod
    def is_visitor(cls, ip_address: str) -> bool:
        return cls.is_active(ip_address)

    @classmethod
    def remove_visitor(cls, ip_address: str) -> None:
        cls._remove(ip_address)

    @classmethod
    def get_visitors(cls) -> list[str]:
        return cls._get_all_ids()


anonymous_tracker = AnonymousTracker()
