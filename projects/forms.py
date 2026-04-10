from django import forms

from core.forms import GithubUrlFormMixin

from .models import Project


class ProjectForm(GithubUrlFormMixin, forms.ModelForm):
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
