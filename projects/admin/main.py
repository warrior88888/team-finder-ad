from django.contrib import admin
from django.utils.html import format_html

from projects.models import Project
from projects.selectors import ProjectSelector
from users.types import UserRequest

from .actions import mark_closed, mark_open


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "status",
        "github_button",
        "participants_count",
        "created_at",
    )
    list_filter = ("status", "created_at", "owner__email")
    list_display_links = ("name",)
    search_fields = ("name", "description", "owner__email")
    autocomplete_fields = ("owner", "participants")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_editable = ("status",)
    list_per_page = 12

    actions = ("mark_open", "mark_closed")

    def get_queryset(self, request):
        return ProjectSelector().list_projects()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("created_at",)
        return ()

    @admin.display(description="Участников", ordering="-id")
    def participants_count(self, obj):
        return obj.participants_count

    @admin.display(description="Github")
    def github_button(self, obj):
        if obj.github_url:
            return format_html(
                '<a href="{}" target="_blank"'
                'class="btn btn-outline-info btn-xs"'
                'title="Открыть репозиторий">'
                '<i class="fab fa-github"></i> Перейти'
                "</a>",
                obj.github_url,
            )
        return "-"

    @admin.action(description="Открыть выбранные")
    def mark_open(self, request: UserRequest, queryset):
        count = mark_open(request, queryset)
        self.message_user(request, f"Открыто проектов: {count}.")

    @admin.action(description="Закрыть выбранные")
    def mark_closed(self, request: UserRequest, queryset):
        count = mark_closed(request, queryset)
        self.message_user(request, f"Закрыто проектов: {count}.")
