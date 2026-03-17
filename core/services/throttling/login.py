import logging

from core.services.redis import ThrottleAction

from .exceptions import OverLimitError
from .limits import LOGIN_FAILS_LIMIT, LOGIN_FAILS_WINDOW
from .throttling import (
    build_key,
    exceed_limit,
    remove_throttled,
    set_throttled,
)

ACTION = ThrottleAction.LOGIN_FAIL

logger = logging.getLogger(__name__)


def build_login_key(email: str, ip: str) -> str:
    """Builds a throttle key scoped to the email + IP pair."""
    return build_key(ACTION, email.lower(), ip or "unknown")


def check_login_attempts(email: str, ip: str) -> None:
    """Raises OverLimitError if the login attempt limit is exceeded."""
    key = build_login_key(email, ip)
    if exceed_limit(key, rate_limit=LOGIN_FAILS_LIMIT):
        logger.warning("Login blocked: email=%s ip=%s", email, ip)
        raise OverLimitError()


def record_login_failure(email: str, ip: str) -> None:
    """Increments the failed login counter for this email + IP pair."""
    key = build_login_key(email, ip)
    count = set_throttled(key, window=LOGIN_FAILS_WINDOW)
    logger.warning(
        "Failed login attempt: email=%s ip=%s attempts=%s/%s",
        email,
        ip,
        count,
        LOGIN_FAILS_LIMIT,
    )


def reset_login_attempts(email: str, ip: str) -> None:
    """Clears the failed login counter after a successful login."""
    key = build_login_key(email, ip)
    remove_throttled(key)
    logger.debug("Login attempts reset: email=%s", email)
