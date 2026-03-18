import io
import logging
import random
import uuid
from pathlib import Path
from typing import Literal

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from pydantic import PositiveInt

from .schemas import AvatarConfig

logger = logging.getLogger(__name__)


class AvatarService:
    """Generates and validates user avatars using Pillow.

    Settings are loaded from Django settings via AvatarConfig schema.
    """

    gen_prefix: str = "av_serv_gen_"

    def __init__(self, config: AvatarConfig | None = None) -> None:
        if config is not None:
            self.config = config
        else:
            raw_data = getattr(settings, "AVATAR_CONFIG", {})
            self.config = AvatarConfig(**raw_data)

    def check_size(self, image) -> bool:
        """Returns True if image is within size limit (or on file access error)."""
        try:
            return image.size <= self.config.max_size_bytes
        except (FileNotFoundError, OSError) as e:
            logger.warning(
                "Avatar size check failed, file not found: %s — %s",
                getattr(image, "name", image),
                e,
            )
            return True

    def generate_avatar(
        self,
        label: str,
        quality: PositiveInt | None = None,
        mode: Literal["PNG", "WEBP"] | None = None,
    ) -> ContentFile:
        """Generates an avatar with the first letter of label.

        Falls back to WEBP at quality=50 if PNG exceeds size limit,
        then to fallback avatar if WEBP still exceeds.
        """
        size = self.config.size
        quality = quality or self.config.quality
        mode = mode or self.config.mode
        bg_color = random.choice(self.config.colors)
        image = Image.new("RGB", size, color=bg_color)
        draw = ImageDraw.Draw(image)
        font = self._get_font()
        letter = label[0].upper()
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) / 2
        vertical_offset = 28  # empirically tuned for the current font size (130px)
        y = (size[1] / 2) - (text_height / 2) - vertical_offset
        draw.text((x, y), letter, fill=(255, 255, 255), font=font)
        buffer = io.BytesIO()
        image.save(buffer, format=mode, quality=quality)
        if buffer.tell() > self.config.max_size_bytes:
            if mode == "PNG":
                logger.warning(
                    (
                        "Avatar size exceeded limit for user: %s. "
                        "Current size: %s MB. Retrying with WEBP..."
                    ),
                    label,
                    self.config.max_size_mb,
                )
                return self.generate_avatar(label=label, quality=50, mode="WEBP")
            else:
                logger.error(
                    (
                        "Avatar generation failed size check for user: %s in %s mode. "
                        "Switching to fallback."
                    ),
                    label,
                    mode,
                )
                return self._set_fallback_avatar(label)
        unique_id = uuid.uuid4().hex[:8]
        filename = (
            f"{self.gen_prefix}{label.split('@')[0]}_{unique_id}_avatar.{mode.lower()}"
        )
        logger.info(
            "Avatar generated successfully for user: %s, filename: %s", label, filename
        )
        return ContentFile(buffer.getvalue(), name=filename)

    @staticmethod
    def file_exists(avatar_field: ContentFile) -> bool:
        """Returns False on storage error rather than raising."""
        try:
            return avatar_field.storage.exists(avatar_field.name)  # type: ignore[reportAttributeAccessIssue]
        except (FileNotFoundError, OSError) as e:
            logger.warning(
                "Avatar file check failed for field '%s': %s",
                avatar_field.name,
                e,
            )
            return False

    def _set_fallback_avatar(self, label: str) -> ContentFile:
        """Returns default avatar, or a gray placeholder if file is missing."""
        default_avatar_path = self.config.default_avatar_path
        try:
            with Path.open(default_avatar_path, "rb") as file:
                logger.info("Using default avatar for user: %s", label)
                return ContentFile(file.read(), name="default_avatar.png")
        except FileNotFoundError:
            logger.error(
                "Default avatar file not found at path: %s", default_avatar_path
            )
            empty_img = Image.new("RGB", self.config.size, color="gray")
            buffer = io.BytesIO()
            empty_img.save(buffer, format="PNG")
            logger.warning("Fallback gray placeholder generated for user: %s", label)
            return ContentFile(buffer.getvalue(), name="fallback.png")

    def _get_font(self) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Returns configured TrueType font, falls back to Pillow default on error."""
        font_path = self.config.font_path
        try:
            return ImageFont.truetype(font_path, 130)
        except OSError:
            logger.error(
                "Failed to load font at: %s. System default font will be used.",
                font_path,
            )
            return ImageFont.load_default()
