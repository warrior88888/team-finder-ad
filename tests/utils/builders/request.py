from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser


class RequestBuilder:
    """Helper for building configured HttpRequest objects in tests."""

    def __init__(self) -> None:
        self.factory = RequestFactory()
        # SessionMiddleware required to initialize request.session
        self._middleware = SessionMiddleware(lambda r: None)  # type: ignore[arg-type]

    def __call__(self, *args: Any, **kwargs: Any) -> HttpRequest:
        """Proxy for create()"""
        return self.create(*args, **kwargs)

    def create(
        self,
        viewname: str = "projects:projects_list",
        user: AbstractBaseUser | None = None,
        data: dict[str, Any] | None = None,
        method: Literal["GET", "POST"] = "GET",
        url_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> HttpRequest:
        """Builds a fully configured HttpRequest by URL name.
        **kwargs for extra Meta Headers e.g. HTTP_X_FORWARDED_FOR='1.2.3.4'
        """
        path = reverse(viewname, kwargs=url_kwargs)
        request = self._build_request(method, path, data, **kwargs)
        self._setup_request(request, user)
        return request

    def _build_request(
        self,
        method: str,
        path: str,
        data: dict[str, Any] | None,
        **kwargs: Any,
    ) -> HttpRequest:
        if method == "POST":
            return self.factory.post(path, data=data or {}, **kwargs)
        return self.factory.get(path, **kwargs)

    def _setup_request(
        self,
        request: HttpRequest,
        user: AbstractBaseUser | None,
    ) -> None:
        self._middleware.process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)  # type: ignore[reportAttributeAccessIssue]
        request.user = user if user else AnonymousUser()
