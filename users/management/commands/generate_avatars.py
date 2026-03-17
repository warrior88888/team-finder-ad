from django.core.management import BaseCommand

from core.services.avatar import AvatarService
from users.selectors import UserSelector


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--blank",
            action="store_true",
            help="Создать аватары для пользователей без аватара",
        )
        parser.add_argument(
            "--default",
            action="store_true",
            help="Создать аватары для пользователей c default_avatar.png",
        )
        parser.add_argument(
            "--fallback",
            action="store_true",
            help="Создать аватары для пользователей c fallback.png",
        )

    def handle(self, *ids: int | str, **options: dict[str, str]):
        blank_flag = bool(options.get("blank"))
        default_flag = bool(options.get("default"))
        fallback_flag = bool(options.get("fallback"))

        selector = UserSelector()

        users_to_fix = selector.get_users_by_avatar(
            blank=blank_flag,
            default=default_flag,
            fallback=fallback_flag,
        )

        count = 0
        avatar_service = AvatarService()

        for user in users_to_fix:
            try:
                user.avatar = avatar_service.generate_avatar(label=user.email)  # type: ignore
                user.save(update_fields=["avatar"])
                count += 1
                self.stdout.write(f"Создан аватар для: {user.pk}")
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Ошибка у {user.pk}: {e}"))
        self.stdout.write(
            self.style.SUCCESS(f"Успешно обновлено пользователей: {count}")
        )
