from django.conf import settings
from django.db import models
from django.urls import reverse

from constants.projects import ProjectFieldLength, ProjectStatus


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN = ProjectStatus.OPEN, "Open"
        CLOSED = ProjectStatus.CLOSED, "Closed"

    name = models.CharField(
        max_length=ProjectFieldLength.NAME,
        verbose_name="Название проекта",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание проекта",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор проекта",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на Github",
    )
    status = models.CharField(
        max_length=max(map(len, Status.values)),
        choices=Status,
        default=Status.OPEN,
        verbose_name="Статус проекта",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники проекта",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:project_detail", kwargs={"project_id": self.pk})
