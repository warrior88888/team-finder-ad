from django.core.management import BaseCommand
from django.urls import reverse

from config import app_config
from config.base import local_ips


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
        domain = app_config.django.domain
        server_name = f"https://{domain}"
        if domain in local_ips:
            server_name = "http://localhost:8000"
        if show_adm or show_all:
            self.stdout.write(
                self.style.SUCCESS(
                    f"URL адрес админ-панели: {server_name}{reverse('admin:index')}"
                )
            )
        if show_ht or show_all:
            self.stdout.write(
                self.style.SUCCESS(
                    f"URL адрес healthcheck: {server_name}{reverse('health_check')}"
                )
            )
