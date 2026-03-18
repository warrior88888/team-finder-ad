from pydantic_settings import BaseSettings, SettingsConfigDict

from config.django import DjangoConfig
from config.logging import LoggingConfig
from config.postgres import PostgresConfig
from config.redis import RedisConfig
from config.task import TaskConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_prefix="TF__",
        env_nested_delimiter="__",
    )

    django: DjangoConfig
    log: LoggingConfig = LoggingConfig()
    postgres: PostgresConfig
    redis: RedisConfig = RedisConfig()
    task: TaskConfig = TaskConfig()


app_config = Settings()  # type: ignore[reportCallIssue]
