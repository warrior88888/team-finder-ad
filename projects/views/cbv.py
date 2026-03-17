from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView

from projects import services
from projects.forms import ProjectForm

from .mixins import (
    IsEditContextMixin,
    OwnerRequiredMixin,
    PaginateMixin,
    ProjectMixin,
    ProjectSuccessUrlMixin,
)

if TYPE_CHECKING:
    from projects.models import Project
    from users.types import UserRequest


class ProjectListView(PaginateMixin):
    template_name = "projects/project_list.html"
    request: UserRequest

    def get_queryset(self):
        return self.selector.list_projects(user=self.request.user)


class ProjectCreateView(
    LoginRequiredMixin,
    IsEditContextMixin,
    ProjectSuccessUrlMixin,
    CreateView,
    ProjectMixin,
):
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    is_edit = False
    request: UserRequest

    def form_valid(self, form: ProjectForm):
        self.object = services.create_project(user=self.request.user, form=form)
        return redirect(self.get_success_url())


class ProjectDetailView(DetailView, ProjectMixin):
    template_name = "projects/project-details.html"
    context_object_name = "project"

    def get_object(self, queryset=None) -> Project:
        pk: int = self.kwargs.get("pk")
        return self.selector.project_detail(project_pk=pk, with_participants=True)


class ProjectUpdateView(
    LoginRequiredMixin,
    OwnerRequiredMixin,
    IsEditContextMixin,
    ProjectSuccessUrlMixin,
    UpdateView,
    ProjectMixin,
):
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    pk_url_kwarg = "pk"
    is_edit = True
    _cached_object: Project | None = None

    def get_object(self, queryset=None) -> Project:
        # Cached to avoid duplicate DB queries
        # between OwnerRequiredMixin and form render
        if self._cached_object is None:
            self._cached_object = self.selector.project_detail(
                project_pk=self.kwargs["pk"]
            )
        return self._cached_object

    def form_valid(self, form: ProjectForm):
        self.object = services.update_project(project=self.get_object(), form=form)
        return redirect(self.get_success_url())
