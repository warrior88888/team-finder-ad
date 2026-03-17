from typing import Any

from factory.declarations import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.helpers import post_generation

from .user import UserFactory


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = "projects.Project"
        skip_postgeneration_save = True

    name = Sequence(lambda n: f"project_{n}")
    description = Faker("text", max_nb_chars=256)
    github_url = Sequence(lambda n: f"https://github.com/{n}")
    owner = SubFactory(UserFactory)

    @post_generation
    def participants(self, create, extracted: Any, **kwargs):
        if not create:
            return
        if extracted is not None:
            for participant in extracted:
                self.participants.add(participant)  # type: ignore[reportAttributeAccessIssue]
        else:
            self.participants.add(self.owner)  # type: ignore[reportAttributeAccessIssue]
