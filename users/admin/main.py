import logging

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.services.activity_tracking import anonymous_tracker, user_tracker
from users.forms import UserRegisterForm
from users.types import UserRequest

from .actions import block_users, unblock_users
from .filters import OnlineStatusFilter
from .forms import AdminUserChangeForm

User = get_user_model()

logger = logging.getLogger(__name__)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserRegisterForm
    form = AdminUserChangeForm
    model = User

    ordering = ("-id",)

    list_display = (
        "get_avatar_thumb",
        "email",
        "get_full_name",
        "get_online_status",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    list_editable = ("is_active",)
    list_filter = (
        OnlineStatusFilter,
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "date_joined",
    )
    list_display_links = ("get_avatar_thumb", "email")
    search_fields = ("email", "name", "surname", "phone")
    readonly_fields = ("last_login", "date_joined", "get_avatar_thumb")
    date_hierarchy = "date_joined"
    list_per_page = 12

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "surname",
                    "get_avatar_thumb",
                    "avatar",
                    "phone",
                    "github_url",
                    "about",
                )
            },
        ),
        (_("Избранное"), {"fields": ("favorites",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password"),
            },
        ),
    )

    filter_horizontal = ("favorites", "groups", "user_permissions")
    actions = ("block_users", "unblock_users")

    class Media:
        css = {"all": ("css/admin_online.css",)}

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["online_users_count"] = user_tracker.get_count()
        extra_context["anonymous_visitors_count"] = anonymous_tracker.get_count()
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description="Аватар")
    def get_avatar_thumb(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 35px; height: 35px;'
                'border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url,
            )
        return "-"

    @admin.display(description="Онлайн")
    def get_online_status(self, obj):
        if user_tracker.is_online(obj):
            return format_html('<span class="online-dot">●</span>')
        return format_html('<span class="offline-dot">●</span>')

    @admin.display(description="Полное имя")
    def get_full_name(self, obj):
        if obj.name:
            return f"{obj.name} {obj.surname}"
        return "-"

    @admin.action(description="Заблокировать выбранных")
    def block_users(self, request: UserRequest, queryset):
        count = block_users(request, queryset)
        self.message_user(
            request, f"Заблокировано пользователей: {count}.", messages.SUCCESS
        )

    @admin.action(description="Разблокировать выбранных")
    def unblock_users(self, request: UserRequest, queryset):
        count = unblock_users(request, queryset)
        self.message_user(
            request, f"Разблокировано пользователей: {count}.", messages.SUCCESS
        )
