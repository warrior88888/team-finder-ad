from pydantic import BaseModel, RedisDsn, SecretStr

from config.base import PortInt


class RedisConfig(BaseModel):
    host: str = "127.0.0.1"
    port: PortInt = 6379
    password: SecretStr
    default_db: int = 0

    def build_dsn(self, db_index: int) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                password=self.pwd,
                path=f"{db_index}",
            )
        )

    @property
    def pwd(self) -> str | None:
        value = self.password.get_secret_value()
        if value.lower() == "no":
            return None
        return value

    @property
    def url(self) -> str:
        return self.build_dsn(self.default_db)
