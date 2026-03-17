from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from health_check.views import HealthCheckView

from config import app_config
from core import views as core_views

handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

urlpatterns = [
    path("", RedirectView.as_view(url="/projects/list/"), name="root"),
    path("auth/", include("django.contrib.auth.urls")),
    path(app_config.django.admin_path, admin.site.urls, name="admin"),
    path("projects/", include("projects.urls")),
    path("users/", include("users.urls")),
    path(
        app_config.django.healthcheck_path,
        HealthCheckView.as_view(
            checks=[
                "health_check.Database",
                "health_check.Storage",
                "health_check.Cache",
            ]
        ),
        name="health_check",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("test403/", core_views.error_403),
        path("test404/", core_views.error_404),
        path("test500/", core_views.error_500),
        path("test429/", core_views.error_429),
        *urlpatterns,
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
