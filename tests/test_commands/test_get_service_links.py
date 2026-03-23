from io import StringIO
from unittest.mock import patch

from django.core.management import call_command

from config import app_config


def test_get_service_links_all():
    out = StringIO()
    call_command("get_service_links", stdout=out)
    output = out.getvalue()
    assert app_config.django.admin_path in output
    assert app_config.django.healthcheck_path in output


def test_get_service_links_adm_only():
    out = StringIO()
    call_command("get_service_links", adm=True, stdout=out)
    output = out.getvalue()
    assert app_config.django.admin_path in output
    assert app_config.django.healthcheck_path not in output


def test_get_service_links_ht_only():
    out = StringIO()
    call_command("get_service_links", ht=True, stdout=out)
    output = out.getvalue()
    assert app_config.django.admin_path not in output
    assert app_config.django.healthcheck_path in output


def test_get_service_links_uses_https_for_domain():
    out = StringIO()
    with patch(
        "core.management.commands.get_service_links.app_config.django.domain",
        "team-finder.ru",
    ):
        call_command("get_service_links", stdout=out)
    assert "https://team-finder.ru" in out.getvalue()


def test_get_service_links_uses_localhost_for_local_ip():
    out = StringIO()
    with (
        patch(
            "core.management.commands.get_service_links.app_config.django.domain",
            "localhost",
        ),
        patch(
            "core.management.commands.get_service_links.local_ips",
            ["localhost"],
        ),
    ):
        call_command("get_service_links", stdout=out)
    assert "http://localhost:8000" in out.getvalue()
