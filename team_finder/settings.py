import logging
from pathlib import Path

from config import app_config

# Core

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = app_config.django.secret_key.get_secret_value()

DEBUG = app_config.django.debug

ALLOWED_HOSTS = app_config.django.allowed_hosts


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "health_check",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "projects",
    "users",
    "core",
]

# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middlewares.ActiveUserMiddleware",
    "core.middlewares.ThrottlingMiddleware",
    "core.middlewares.OnlineStatusTrackingMiddleware",
]

# URLs / WSGI

ROOT_URLCONF = "team_finder.urls"

WSGI_APPLICATION = "team_finder.wsgi.application"

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / f"templates_var{app_config.task.version}"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database

DATABASES = {"default": app_config.postgres.django_db_dict}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": app_config.redis.url,
    },
}

# Sessions

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Authentication

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

AUTH_PASSWORD_VALIDATORS = []
if not DEBUG:
    AUTH_PASSWORD_VALIDATORS.extend(
        [
            {
                "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
            },
            {
                "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
            },
            {
                "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
            },
            {
                "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
            },
        ]
    )

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "projects:projects_list"

# Security

CSRF_TRUSTED_ORIGINS = app_config.django.csrf_trusted_origins

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Internalization

LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & Media

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collected_static"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Logging

LOGS_DIR = Path("/var/log/django")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": app_config.log.format,
        },
    },
    "filters": {
        "info_only": {
            "()": "core.services.log.filters.InfoOnlyFilter",
        },
        "warning_and_above": {
            "()": "core.services.log.filters.WarningAndAboveFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "filename": LOGS_DIR / "info.log",
            "maxBytes": 1024 * 1024 * 16,
            "backupCount": 3,
            "encoding": "utf-8",
            "filters": ["info_only"],
        },
        "file_warning": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "filename": LOGS_DIR / "warning.log",
            "maxBytes": 1024 * 1024 * 16,
            "backupCount": 3,
            "encoding": "utf-8",
            "filters": ["warning_and_above"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file_info", "file_warning"],
            "level": app_config.log.level,
        },
        "django": {
            "handlers": ["console", "file_info", "file_warning"],
            "level": app_config.log.django_level,
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "file_info", "file_warning"],
            "level": app_config.log.db_level,
            "propagate": False,
        },
    },
}

# Throttling

THROTTLE_LOGIN_FAILS_LIMIT = 7
THROTTLE_LOGIN_FAILS_RESET_WINDOW = 180

THROTTLE_RATE_LIMIT = 100
THROTTLE_WINDOW = 60

THROTTLE_AVATAR_RATE_LIMIT = 5
THROTTLE_AVATAR_RESET_WINDOW = 60

# Custom Middleware (core.services.middlewares.BaseMiddleware)

SERVICES_SKIP_PATHS = [
    STATIC_URL,
    MEDIA_URL,
    "/__debug__/",
    "/favicon.ico",
    app_config.django.healthcheck_path,
    "/robots.txt",
]

SERVICES_SKIP_IPS = ("127.0.0.1", "::1")

SERVICES_SKIP_IP_PREFIXES = ("172.", "192.168.", "10.")

# Avatar Service

AVATAR_CONFIG = {
    "max_size_mb": 5.0,
    "size": (200, 200),
    "mode": "PNG",
    "quality": 90,
    "font_path": BASE_DIR
    / "static"
    / "fonts"
    / "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf",
    "default_avatar_path": BASE_DIR / "static" / "images" / "default-avatar.png",
    "colors": [
        (173, 216, 230),
        (255, 222, 173),
        (211, 211, 211),
        (144, 238, 144),
        (255, 182, 193),
        (221, 160, 221),
    ],
}

# Jazzmin AdminPanel

JAZZMIN_SETTINGS = {
    "site_title": "TeamFinder Admin",
    "site_header": "TeamFinder",
    "site_brand": "Team Finder",
    "welcome_sign": "Панель управления TeamFinder",
    "copyright": "TeamFinder Ltd",
    "search_model": ["users.User", "projects.Project"],
    "user_avatar": "avatar",
    "usermenu_links": [
        {
            "name": "Открыть сайт",
            "url": "/",
            "new_window": True,
            "icon": "fas fa-external-link-alt",
        },
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["core"],
    "hide_models": [],
    "icons": {
        "auth.Group": "fas fa-users-cog",
        "users.User": "fas fa-user",
        "projects.Project": "fas fa-rocket",
    },
    "order_with_respect_to": ["users", "projects", "auth"],
    "show_ui_builder": DEBUG,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "layout_fixed": False,
    "actions_sticky_top": False,
}

# Settings mutation for DEBUG

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
    INTERNAL_IPS = ["127.0.0.1", "localhost", "django_app", "nginx_container"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }
    SERVICES_SKIP_PATHS += [STATIC_URL, MEDIA_URL]
    SERVICES_SKIP_IPS = ()
    SERVICES_SKIP_IP_PREFIXES = ()
    STORAGES["staticfiles"]["BACKEND"] = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": app_config.log.format,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": app_config.log.level,
            },
            "django": {
                "handlers": ["console"],
                "level": app_config.log.level,
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": app_config.log.db_level,
                "propagate": False,
            },
        },
    }
