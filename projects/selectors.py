from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Count, Exists, OuterRef, QuerySet, Value
from django.http import Http404

from .models import Project

if TYPE_CHECKING:
    from users.models import User as UserModel


class ProjectSelector:
    """Read-only interface for Project queries.

    Encapsulates annotations, subqueries, and N+1 optimizations.
    """

    @staticmethod
    def _get_base_queryset() -> QuerySet[Project]:
        queryset = (
            Project.objects.all()
            .select_related("owner")
            .prefetch_related("participants")
            .annotate(participants_count=Count("participants", distinct=True))
            .order_by("-created_at")
        )
        return queryset

    def list_projects(
        self, *, user: UserModel | None = None, favorites_only: bool = False
    ) -> QuerySet[Project]:
        """Returns projects annotated with is_favorite for the given user.

        If favorites_only=True, returns only projects the user has favorited.
        """
        queryset = self._get_base_queryset()
        if favorites_only and user and user.is_authenticated:
            queryset = queryset.filter(interested_users=user).annotate(
                is_favorite=Value(True)
            )
        elif user and user.is_authenticated:
            is_favorite_subquery = user.favorites.filter(pk=OuterRef("pk"))
            queryset = queryset.annotate(is_favorite=Exists(is_favorite_subquery))
        else:
            queryset = queryset.annotate(is_favorite=Value(False))
        return queryset

    def project_detail(
        self,
        *,
        project_pk: int,
        with_participants: bool = False,
    ) -> Project:
        """Returns a Project by pk, raises Http404 if not found.

        with_participants=True includes participants_count annotation.
        """
        try:
            if with_participants:
                return self._get_base_queryset().get(pk=project_pk)
            return Project.objects.select_related("owner").get(pk=project_pk)
        except Project.DoesNotExist:
            raise Http404("Такого проекта не существует") from None
