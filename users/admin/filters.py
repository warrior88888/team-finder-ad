from django.contrib import admin
from django.core.cache import cache

from core.services.activity_tracking import user_tracker


class OnlineStatusFilter(admin.SimpleListFilter):
    title = "Статус онлайн"
    parameter_name = "online"
    CACHE_KEY = "admin:online_users_ids"
    CACHE_TTL = 30

    def lookups(self, request, model_admin):
        return (
            ("yes", "Онлайн"),
            ("no", "Оффлайн"),
        )

    def _get_online_ids(self) -> list[int]:
        ids = cache.get(self.CACHE_KEY)
        if ids is None:
            ids = user_tracker.get_online_users_ids()
            cache.set(self.CACHE_KEY, ids, self.CACHE_TTL)
        return ids

    def queryset(self, request, queryset):
        online_ids = self._get_online_ids()
        if self.value() == "yes":
            return queryset.filter(pk__in=online_ids)
        if self.value() == "no":
            return queryset.exclude(pk__in=online_ids)
        return queryset
