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
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path(
        "<int:pk>/edit/",
        views.ProjectUpdateView.as_view(),
        name="edit_project",
    ),
    path(
        "<int:pk>/toggle-favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    path(
        "<int:pk>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
    path("<int:pk>/complete/", views.complete_project, name="complete_project"),
]
