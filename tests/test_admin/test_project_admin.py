import pytest
from django.contrib.admin.sites import AdminSite

from projects.admin import ProjectAdmin
from projects.models import Project

pytestmark = pytest.mark.django_db


@pytest.fixture
def model_admin():
    return ProjectAdmin(Project, AdminSite())


def test_mark_closed(model_admin, admin_request, project_factory):
    p1 = project_factory(status="open")
    p2 = project_factory(status="open")
    queryset = Project.objects.filter(pk__in=[p1.pk, p2.pk])
    model_admin.mark_closed(admin_request, queryset)
    p1.refresh_from_db()
    p2.refresh_from_db()
    assert p1.status == Project.Status.CLOSED
    assert p2.status == Project.Status.CLOSED


def test_mark_open(model_admin, admin_request, project_factory):
    p1 = project_factory(status="closed")
    queryset = Project.objects.filter(pk=p1.pk)
    model_admin.mark_open(admin_request, queryset)
    p1.refresh_from_db()
    assert p1.status == Project.Status.OPEN
