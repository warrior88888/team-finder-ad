from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from core.services.redis import ThrottleAction
from core.services.throttling import limits, throttle_endpoint
from users import services
from users.types import UserRequest


@login_required
def user_logout(request: UserRequest):
    services.logout_user(request)
    return redirect("projects:projects_list")


@require_POST
@login_required
@throttle_endpoint(
    action=ThrottleAction.AVATAR_RESET,
    rate_limit=limits.AVATAR_RESET_RATE_LIMIT,
    window=limits.AVATAR_RESET_WINDOW,
)
def reset_user_avatar(request: UserRequest):
    avatar_url = services.reset_avatar(request=request)
    return JsonResponse({"avatar_url": avatar_url})
