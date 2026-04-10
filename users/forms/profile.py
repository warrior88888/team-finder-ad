from django import forms
from django.contrib.auth import get_user_model

from core.forms import GithubUrlFormMixin
from core.validators import check_avatar_size, normalize_and_check_phone

User = get_user_model()


class UserEditForm(GithubUrlFormMixin, forms.ModelForm):
    """Form for editing user's profile."""

    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "avatar": forms.FileInput(attrs={"class": "form-control-file"}),
            "about": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Расскажите о своих навыках...",
                }
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "89991234567"}
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username",
                }
            ),
        }

    def clean_avatar(self) -> str | None:
        avatar = self.cleaned_data.get("avatar")
        if avatar and not check_avatar_size(avatar):
            raise forms.ValidationError("Размер файла не должен превышать 5 МБ")
        return avatar

    def clean_phone(self) -> str | None:
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone
        normalized, is_valid, is_unique = normalize_and_check_phone(
            phone, exclude_user_id=self.instance.pk
        )
        if not is_valid:
            raise forms.ValidationError("Неверный формат номера.")
        if not is_unique:
            raise forms.ValidationError("Пользователь с таким номером уже существует")
        return normalized
