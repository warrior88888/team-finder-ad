import logging

from projects.models import Project
from users.types import UserRequest

logger = logging.getLogger(__name__)


def mark_open(request: UserRequest, queryset):
    projects = list(queryset)
    count = queryset.update(status=Project.Status.OPEN)
    for project in projects:
        logger.info(
            "Project marked open by admin: pk=%s name=%s admin=%s",
            project.pk,
            request.user.pk,
        )
    return count


def mark_closed(request: UserRequest, queryset) -> int:
    projects = list(queryset)
    count = queryset.update(status=Project.Status.CLOSED)
    for project in projects:
        logger.info(
            "Project marked closed by admin: pk=%s admin=%s",
            project.pk,
            request.user.pk,
        )
    return count
