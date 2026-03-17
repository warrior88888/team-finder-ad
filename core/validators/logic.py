import re

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from core.services.avatar import AvatarService

User = get_user_model()


def check_avatar_size(avatar: ContentFile) -> bool:
    avatar_service = AvatarService()
    return avatar_service.check_size(avatar)


def check_email_unique(email: str, exclude_user_id: int = 0) -> bool:
    """Checks email uniqueness case-insensitively.

    exclude_user_id skips that user — useful when editing an existing profile.
    """
    qs = User.objects.filter(email__iexact=email)
    if exclude_user_id:
        qs = qs.exclude(id=exclude_user_id)
    return not qs.exists()


def check_github_url(url: str | None) -> tuple[bool, str | None]:
    """Validates a GitHub profile URL.

    Returns (True, None) on success, or (False, error_code) where
    error_code is 'not_github' or 'no_protocol'.
    """
    if not url:
        return True, None
    if "github.com" not in url.lower():
        return False, "not_github"
    if not url.startswith("https://"):
        return False, "no_protocol"
    return True, None


def normalize_and_check_phone(
    phone: str, exclude_user_id: int = 0
) -> tuple[str, bool, bool]:
    """Normalizes phone to +7... format and checks validity and uniqueness."""
    if not re.match(r"^(\+7|8)\d{10}$", phone):
        return phone, False, False

    normalized = "+7" + phone[1:] if phone.startswith("8") else phone
    qs = User.objects.filter(phone=normalized)
    if exclude_user_id:
        qs = qs.exclude(id=exclude_user_id)
    is_unique = not qs.exists()
    return normalized, True, is_unique
