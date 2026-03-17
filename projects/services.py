from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.db import transaction

from projects.models import Project

if TYPE_CHECKING:
    from projects.forms import ProjectForm
    from users.models import User as UserModel


logger = logging.getLogger(__name__)


@transaction.atomic
def create_project(*, user: UserModel, form: ProjectForm) -> Project:
    """Creates a project, sets owner, and adds them as the first participant."""
    form.instance.owner = user
    project: Project = form.save()
    project.participants.add(user)
    logger.info(
        "Project created successfully: ID=%s by user_id=%s",
        project.pk,
        user.pk,
    )
    return project


def update_project(*, project: Project, form: ProjectForm) -> Project:
    """Updates project data from a validated form."""
    form.instance = project
    project = form.save()
    logger.info("Project updated successfully: ID=%s", project.pk)
    return project


def toggle_project_favorite(*, user: UserModel, project: Project) -> bool:
    """Toggles favorite status. Returns True if added, False if removed."""
    favorites = user.favorites
    if favorites.filter(pk=project.pk).exists():
        favorites.remove(project)
        logger.debug(
            "Project ID=%s removed from favorites by user_id=%s",
            project.pk,
            user.pk,
        )
        return False
    favorites.add(project)
    logger.debug(
        "Project ID=%s added to favorites by user_id=%s",
        project.pk,
        user.pk,
    )
    return True


def toggle_project_participate(
    *, user: UserModel, project: Project
) -> tuple[bool, int]:
    """Toggles participation. Returns (is_participating, participants_count).

    Owner is always considered a participant — their status is never changed.
    """
    if project.owner == user:
        return (
            True,
            project.participants.count(),
        )
    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participating = False
        logger.debug(
            "User_id=%s left project ID=%s",
            user.pk,
            project.pk,
        )
    else:
        project.participants.add(user)
        participating = True
        logger.debug(
            "User_id=%s joined project ID=%s",
            user.pk,
            project.pk,
        )

    participants_count = project.participants.count()
    return participating, participants_count


def owner_complete_project(*, project: Project, user: UserModel) -> str:
    """Sets project status to closed. Only the owner can do this.

    Raises:
        PermissionDenied: if user is not the owner.
        ValueError: if project is already closed.
    """
    if project.owner != user:
        logger.warning(
            "Unauthorized project closure attempt: project_id=%s by user_id=%s",
            project.pk,
            user.pk,
        )
        raise PermissionDenied("Only owner can complete project")
    if project.status == Project.Status.CLOSED:
        raise ValueError("Project is already closed")
    project.status = Project.Status.CLOSED
    project.save(update_fields=["status"])
    logger.info(
        "Project ID=%s completed by owner user_id=%s",
        project.pk,
        user.pk,
    )
    return project.status
