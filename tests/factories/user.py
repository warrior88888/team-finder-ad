from typing import TypeVar

from django.db import models
from factory.declarations import Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker

M = TypeVar("M", bound=models.Model)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "users.User"
        django_get_or_create = ("email",)

    email = Sequence(lambda n: f"user_{n}@example.com")
    name = Faker("first_name", locale="ru_RU")
    surname = Faker("last_name", locale="ru_RU")
    phone = Sequence(lambda n: f"+7999{n:07d}")
    github_url = Sequence(lambda n: f"https://github.com/{n}")
    about = Faker("text", max_nb_chars=256)
    is_active = True
    is_staff = False
    is_superuser = False

    @classmethod
    def _create(cls, model_class: M, *args, **kwargs) -> M:
        manager = cls._get_manager(model_class)
        if "password" not in kwargs:
            kwargs["password"] = "x*bR%N72:5"
        return manager.create_user(*args, **kwargs)
