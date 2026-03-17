from django.http import HttpRequest

from core.utils import get_client_ip, should_skip


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def should_skip(request: HttpRequest, skip_staff: bool = True) -> bool:
        return should_skip(request, skip_staff=skip_staff)

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        return get_client_ip(request)
