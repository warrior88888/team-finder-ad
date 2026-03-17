from pydantic import BaseModel


class TaskConfig(BaseModel):
    version: int = 1
