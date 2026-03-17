import logging

from core.services.activity_tracking import user_tracker
from users.types import UserRequest

logger = logging.getLogger(__name__)


def block_users(request: UserRequest, queryset) -> int:
    users = list(queryset)
    count = queryset.update(is_active=False)
    for user in users:
        user_tracker.remove_online(user)
        logger.info(
            "User: %s was blocked by admin: %s",
            user.pk,
            request.user.pk,
        )
    return count


def unblock_users(request, queryset) -> int:
    users = list(queryset)
    count = queryset.update(is_active=True)
    for user in users:
        logger.info(
            "User: %s was unblocked by admin: %s",
            user.pk,
            request.user.pk,
        )
    return count
