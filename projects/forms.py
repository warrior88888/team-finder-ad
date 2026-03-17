from django import forms
from django.contrib.auth import get_user_model

from core.validators import check_github_url

from .models import Project

User = get_user_model()


class ProjectForm(forms.ModelForm):
    """Form for creating and updating project."""

    status = forms.ChoiceField(
        choices=[
            (Project.Status.OPEN, "Открытый"),
            (Project.Status.CLOSED, "Закрытый"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Расскажите о проекте...",
                }
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/project",
                }
            ),
        }

    def clean_github_url(self) -> str | None:
        url = self.cleaned_data.get("github_url")
        is_valid, error = check_github_url(url)
        if not is_valid:
            if error == "not_github":
                raise forms.ValidationError("Ссылка должна вести на GitHub")
            if error == "no_protocol":
                raise forms.ValidationError("Ссылка должна начинаться с https://")
        return url
