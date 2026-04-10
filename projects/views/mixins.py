from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from constants import PageSize
from projects.models import Project
from projects.selectors import ProjectSelector

if TYPE_CHECKING:
    from users.types import UserRequest


class ProjectMixin:
    """Provides shared model and selector for project views."""

    model = Project
    selector = ProjectSelector()


class ProjectSuccessUrlMixin:
    """Redirects to project detail page after a successful action."""

    object: Project

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class PaginateMixin(ListView, ProjectMixin):
    paginate_by = PageSize.PROJECTS
    context_object_name = "projects"


class OwnerRequiredMixin(UserPassesTestMixin):
    """Restricts access to the project owner only.

    Non-owners are redirected to the project detail page.
    Unauthenticated users are redirected to login.
    """

    request: UserRequest
    kwargs: dict[str, int]

    def get_object(self, queryset=None) -> Project: ...

    def test_func(self) -> bool:
        return self.request.user == self.get_object().owner

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect(
                "projects:project_detail", project_id=self.kwargs["project_id"]
            )
        return redirect_to_login(
            self.request.get_full_path(),
            login_url=reverse("users:login"),
        )


class IsEditContextMixin:
    """Passes is_edit flag to template context."""

    is_edit: bool = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # type: ignore[misc]
        context["is_edit"] = self.is_edit
        return context
