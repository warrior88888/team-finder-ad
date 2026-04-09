from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from projects import services
from projects.models import Project

if TYPE_CHECKING:
    from users.types import UserRequest


@login_required
@require_POST
def toggle_favorite(request: UserRequest, pk: int):
    project = get_object_or_404(Project, pk=pk)
    favorited = services.toggle_project_favorite(project=project, user=request.user)
    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
@require_POST
def toggle_participate(request: UserRequest, pk: int):
    project = get_object_or_404(Project, pk=pk)
    participating, participants_count = services.toggle_project_participate(
        project=project, user=request.user
    )
    return JsonResponse(
        {
            "status": "ok",
            "participating": participating,
            "participants_count": participants_count,
        }
    )


@login_required
@require_POST
def complete_project(request: UserRequest, pk: int):
    """Returns 403 on PermissionDenied, 400 on ValueError."""
    project = get_object_or_404(Project, pk=pk)
    try:
        project_status = services.owner_complete_project(
            project=project, user=request.user
        )
        return JsonResponse({"status": "ok", "project_status": project_status})
    except PermissionDenied as exception:
        return JsonResponse({"error": str(exception)}, status=HTTPStatus.FORBIDDEN)
    except ValueError as exception:
        return JsonResponse({"error": str(exception)}, status=HTTPStatus.BAD_REQUEST)
