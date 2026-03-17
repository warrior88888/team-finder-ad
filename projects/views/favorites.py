from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import PaginateMixin

if TYPE_CHECKING:
    from users.types import UserRequest


class FavoritesListView(LoginRequiredMixin, PaginateMixin):
    template_name = "projects/favorite_projects.html"
    request: UserRequest

    def get_queryset(self):
        user = self.request.user
        return self.selector.list_projects(user=user, favorites_only=True)
