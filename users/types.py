from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.http import HttpRequest

from .models import User


class AuthenticatedUser[U: AbstractUser](HttpRequest):
    user: U


AnyUser = User | AnonymousUser
UserRequest = AuthenticatedUser[User]
