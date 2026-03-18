from pydantic import BaseModel, PostgresDsn, SecretStr

from config.base import PortInt


class PostgresConfig(BaseModel):
    db: str = "teamfinder"
    host: str = "localhost"
    port: PortInt = 5432
    user: str = "postgres"
    password: SecretStr

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.user,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )

    @property
    def django_db_dict(self) -> dict[str, str | int]:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": self.db,
            "USER": self.user,
            "PASSWORD": self.password.get_secret_value(),
            "HOST": self.host,
            "PORT": self.port,
        }
