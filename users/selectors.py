from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, Q, QuerySet
from django.http import Http404

from core.services.avatar import AvatarService
from projects.models import Project

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser

    from users.models import User as UserModel

User = get_user_model()


class UserSelector:
    """Read-only interface for user queries with complex filtering and prefetching."""

    _PARTICIPANT_FILTERS: dict[str, str] = {
        "owners-of-favorite-projects": "owned_projects__interested_users",
        "owners-of-participating-projects": "owned_projects__participants",
        "interested-in-my-projects": "favorites__owner",
        "participants-of-my-projects": "participated_projects__owner",
    }

    @staticmethod
    def _get_base_queryset() -> QuerySet[AbstractBaseUser]:
        return User.objects.all()

    def participants_list(
        self,
        *,
        filter_by: str | None = None,
        user: UserModel | None = None,
    ) -> QuerySet[AbstractBaseUser]:
        """Returns users optionally filtered by relationship to request_user.

        Args:
            filter_by: Supported values:
                - ``owners-of-favorite-projects``: owners of projects I favorited.
                - ``owners-of-participating-projects``: owners of projects I joined.
                - ``interested-in-my-projects``: users who favorited my projects.
                - ``participants-of-my-projects``: participants in my projects.
            user: Filter is skipped if None or unauthenticated.
        """
        queryset = self._get_base_queryset()
        lookup = self._PARTICIPANT_FILTERS.get(filter_by) if filter_by else None
        if lookup and user:
            queryset = queryset.filter(**{lookup: user})
        return queryset.distinct()

    @staticmethod
    def user_details(*, user_pk) -> AbstractBaseUser:
        """Returns user with prefetched owned projects and participants count.

        Raises:
            Http404: If user is not found.
        """
        try:
            return User.objects.prefetch_related(
                Prefetch(
                    "owned_projects",
                    queryset=Project.objects.annotate(
                        participants_count=Count("participants", distinct=True)
                    ),
                )
            ).get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404("Такого пользователя не существует") from None

    def get_users_by_avatar(
        self,
        *,
        user_ids: list[int] | None = None,
        blank: bool = False,
        default: bool = False,
        fallback: bool = False,
        generated: bool = False,
        personal: bool = False,
    ) -> QuerySet[AbstractBaseUser]:
        """Returns users filtered by avatar type.

        Args:
            user_ids: Optional list of user IDs to narrow the search.
            blank: Users with no avatar set.
            default: Users with the default placeholder avatar.
            fallback: Users with the gray fallback avatar.
            generated: Users with an auto-generated avatar.
            personal: Users with a manually uploaded avatar (excludes all system names).

        Raises:
            ValueError: If no filter condition is provided.
        """
        if not any((blank, default, fallback, generated, personal)) and not user_ids:
            raise ValueError("Условия для фильтрации не переданы")
        query = Q()
        queryset = self._get_base_queryset()
        prefix = AvatarService.gen_prefix
        if blank:
            query |= Q(avatar__isnull=True) | Q(avatar="")
        if default:
            query |= Q(avatar__icontains="default_avatar.png")
        if fallback:
            query |= Q(avatar__icontains="fallback.png")
        if generated:
            query |= Q(avatar__icontains=prefix)
        if personal:
            personal_query = (
                ~Q(avatar="")
                & ~Q(avatar__isnull=True)
                & ~Q(avatar__icontains="default_avatar.png")
                & ~Q(avatar__icontains="fallback.png")
                & ~Q(avatar__icontains=prefix)
            )
            query |= personal_query
        if user_ids:
            queryset = queryset.filter(pk__in=user_ids)
        users_to_update = queryset.filter(query).distinct()
        return users_to_update
