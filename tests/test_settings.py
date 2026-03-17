from pathlib import Path

from config import app_config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test"

ALLOWED_HOSTS = ["*"]

# Turn off debug mode for Testing

DEBUG = False

# Application definition

INSTALLED_APPS = [
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

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "team_finder.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates_var1"],
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

WSGI_APPLICATION = "team_finder.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Cache (fakeredis)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": app_config.redis.url,
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Session

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Throttling
THROTTLE_RATE_LIMIT = 100_000
THROTTLE_WINDOW = 10

THROTTLE_LOGIN_FAILS_LIMIT = 100_000
THROTTLE_LOGIN_FAILS_RESET_WINDOW = 10

THROTTLE_AVATAR_RESET_RATE_LIMIT = 100_000
THROTTLE_AVATAR_RESET_WINDOW = 10

# Middleware skip lists
MIDDLEWARE_SKIP_PATHS = []
MIDDLEWARE_SKIP_IPS = []
MIDDLEWARE_SKIP_IP_PREFIXES = ()

# Test Settings For Avatar Service

AVATAR_CONFIG = {
    "max_size_mb": 1,
    "size": (10, 10),
    "mode": "PNG",
    "quality": 10,
    "font_path": BASE_DIR
    / "static"
    / "fonts"
    / "Neue_Haas_Grotesk_Display_Pro_75_Bold.otf",
    "default_avatar_path": BASE_DIR / "static" / "images" / "default-avatar.png",
    "colors": [(0, 0, 0)],
}

# Login
LOGIN_URL = "users:login"

LOGIN_REDIRECT_URL = "projects:projects_list"

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "collected_static"

STATICFILES_DIRS = [BASE_DIR / "static"]


# Service Routs

ADMIN_PATH = "admin"
HEALTHCHECK_PATH = "ht"

# Media files

MEDIA_URL = "/test_media/"
MEDIA_ROOT = BASE_DIR / "test_media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
