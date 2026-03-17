from pydantic import BaseModel

from .base import LogLevel


class LoggingConfig(BaseModel):
    format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"  # noqa: E501
    level: LogLevel = "INFO"
    db_level: LogLevel = "WARNING"
    django_level: LogLevel = "INFO"
