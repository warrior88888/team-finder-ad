from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxLengthValidator
from django.db import models

from core.services.avatar import AvatarService

from .managers import UserManager

_avatar_service = AvatarService()


class User(AbstractUser):
    """Custom user model with email auth and auto-generated avatars.

    username is removed; email is the USERNAME_FIELD.
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )
    name = models.CharField(
        max_length=124,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=124,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватарка",
    )
    phone = models.CharField(
        unique=True,
        max_length=12,
        verbose_name="Телефон",
        blank=True,
        null=True,
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Github",
    )
    about = models.TextField(
        blank=True,
        null=True,
        verbose_name="О себе",
        max_length=256,
        validators=[MaxLengthValidator(256)],
    )
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные проекты",
    )

    objects: UserManager

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = _avatar_service.generate_avatar(label=str(self))
        else:
            # Regenerate only if file is missing — skip for fresh uploads
            try:
                is_new_upload = isinstance(self.avatar.file, UploadedFile)
            except (FileNotFoundError, OSError):
                is_new_upload = False
            if not is_new_upload and not _avatar_service.file_exists(self.avatar):
                self.avatar = _avatar_service.generate_avatar(label=str(self))
            elif is_new_upload and self.pk:
                # Delete old avatar
                try:
                    old = User.objects.get(pk=self.pk)
                    if old.avatar:
                        old.avatar.delete(save=False)  # type: ignore[reportAttributeAccessIssue]
                except User.DoesNotExist:
                    pass
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]
