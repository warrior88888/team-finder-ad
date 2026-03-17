from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    FilePath,
    PositiveFloat,
    PositiveInt,
    field_validator,
)


class AvatarConfig(BaseModel):
    """Pydantic schema for avatar generation settings from Django settings.

    Validates types, positive dimensions, and existence of font/default_avatar files.
    """

    max_size_mb: PositiveFloat
    size: tuple[PositiveInt, PositiveInt]
    mode: Literal["PNG", "WEBP"]
    quality: PositiveInt = Field(default=90, ge=1, le=100)
    font_path: FilePath
    default_avatar_path: FilePath
    colors: list[tuple[int, int, int]]

    @field_validator("colors")
    @classmethod
    def validate_colors(cls, colors):
        for color in colors:
            if not all(0 <= c <= 255 for c in color):
                raise ValueError(f"RGB values must be between 0 and 255, got {color}")
        return colors

    @property
    def max_size_bytes(self) -> int:
        return int(self.max_size_mb * 1024 * 1024)
