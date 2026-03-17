from pydantic import BaseModel, SecretStr

from .base import local_ips


class DjangoConfig(BaseModel):
    debug: bool = False
    domain: str = "localhost"
    secret_key: SecretStr
    admin_path: str = "admin/"
    healthcheck_path: str = "ht/"

    @property
    def allowed_hosts(self) -> list[str]:
        hosts = ["django_app", "nginx_container", "localhost"]
        if self.debug or self.domain in local_ips:
            return [*hosts, *local_ips]
        return [*hosts, self.domain, f"www.{self.domain}"]

    @property
    def csrf_trusted_origins(self) -> list[str]:
        if self.debug or self.domain in local_ips:
            return [f"http://{ip}:8000" for ip in local_ips]
        return [f"https://{self.domain}"]
