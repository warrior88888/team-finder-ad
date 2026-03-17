from core.services.activity_tracking import anonymous_tracker, user_tracker

from .base import BaseMiddleware


class OnlineStatusTrackingMiddleware(BaseMiddleware):
    def __call__(self, request):
        if not self.should_skip(request, skip_staff=False):
            if request.user.is_authenticated:
                user_tracker.mark_online(request.user)
            else:
                ip = self.get_client_ip(request)
                anonymous_tracker.mark_visitor(ip)

        return self.get_response(request)
