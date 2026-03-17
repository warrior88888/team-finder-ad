from django.core.management import BaseCommand
from django.urls import reverse


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--adm", action="store_true", help="Показать URL админ-панели"
        )

        parser.add_argument(
            "--ht", action="store_true", help="Показать URL healthcheck"
        )

    def handle(self, *args, **options: dict[str, str]) -> None:
        show_adm = options.get("adm")
        show_ht = options.get("ht")
        show_all = not any((show_adm, show_ht))

        if show_adm or show_all:
            self.stdout.write(
                self.style.SUCCESS(
                    f"URL адрес админ-панели: http://localhost:8000{reverse('admin:index')}"
                )
            )
        if show_ht or show_all:
            self.stdout.write(
                self.style.SUCCESS(
                    f"URL адрес healthcheck: http://localhost:8000{reverse('health_check')}"
                )
            )
