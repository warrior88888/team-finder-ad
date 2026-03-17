from .cbv import (
    ProjectCreateView,
    ProjectDetailView,
    ProjectListView,
    ProjectUpdateView,
)
from .endpoints import complete_project, toggle_favorite, toggle_participate
from .favorites import FavoritesListView

__all__ = [
    "FavoritesListView",
    "ProjectCreateView",
    "ProjectDetailView",
    "ProjectListView",
    "ProjectUpdateView",
    "complete_project",
    "toggle_favorite",
    "toggle_participate",
]
