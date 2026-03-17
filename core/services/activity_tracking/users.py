from django.contrib.auth.models import AbstractUser

from core.services.redis import RedisPrefix

from .base import BaseTracker


class UserOnlineStatusTracker(BaseTracker):
    """Tracks online status of authenticated users."""

    PREFIX = RedisPrefix.ONLINE

    @classmethod
    def mark_online(cls, user: AbstractUser) -> None:
        cls._set(user.pk)

    @classmethod
    def is_online(cls, user: AbstractUser) -> bool:
        return cls.is_active(user.pk)

    @classmethod
    def remove_online(cls, user: AbstractUser) -> None:
        cls._remove(user.pk)

    @classmethod
    def get_online_users_ids(cls) -> list[int]:
        return [int(uid) for uid in cls._get_all_ids()]


user_tracker = UserOnlineStatusTracker()
