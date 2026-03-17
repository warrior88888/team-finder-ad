from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from core.validators import check_email_unique

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Придумайте пароль"}
        ),
        label="Пароль",
    )

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иван"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Иванов"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@mail.com",
                }
            ),
        }

    def clean_password(self):
        password = self.cleaned_data["password"]
        try:
            validate_password(password, self.instance)
        except ValidationError as error:
            raise forms.ValidationError(error.messages) from error
        return password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not check_email_unique(email, exclude_user_id=self.instance.pk):
            raise forms.ValidationError("Пользователь с таким Email уже существует")
        return email.lower()

    def save(self, commit=True):
        # Hashing password before saving
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
        return user
