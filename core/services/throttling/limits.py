from django.conf import settings

RATE_LIMIT: int = getattr(settings, "THROTTLE_RATE_LIMIT", 100)
WINDOW: int = getattr(settings, "THROTTLE_WINDOW", 60)

LOGIN_FAILS_LIMIT: int = getattr(settings, "THROTTLE_LOGIN_FAILS_LIMIT", 10)
LOGIN_FAILS_WINDOW: int = getattr(settings, "THROTTLE_LOGIN_FAILS_RESET_WINDOW", 10)

AVATAR_RESET_RATE_LIMIT: int = getattr(settings, "THROTTLE_AVATAR_RATE_LIMIT", 5)
AVATAR_RESET_WINDOW: int = getattr(settings, "THROTTLE_AVATAR_RESET_WINDOW", 60)
