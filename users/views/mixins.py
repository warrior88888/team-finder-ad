from django.contrib.auth import get_user_model
from django.urls import reverse

from users.selectors import UserSelector
from users.types import UserRequest

User = get_user_model()


class UserMixin:
    """Provides shared model and selector for user views."""

    model = User
    selector = UserSelector()


class UserSuccessUrlMixin:
    """Redirects to the current user's profile page after a successful action."""

    request: UserRequest

    def get_success_url(self) -> str:
        return reverse("users:user_detail", kwargs={"pk": self.request.user.pk})
