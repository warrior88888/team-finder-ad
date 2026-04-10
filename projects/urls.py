from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("list/", views.ProjectListView.as_view(), name="projects_list"),
    path(
        "create-project/",
        views.ProjectCreateView.as_view(),
        name="create_project",
    ),
    path("favorites/", views.FavoritesListView.as_view(), name="favorites"),
    path("<int:project_id>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path(
        "<int:project_id>/edit/",
        views.ProjectUpdateView.as_view(),
        name="edit_project",
    ),
    path(
        "<int:project_id>/toggle-favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "<int:project_id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
]
