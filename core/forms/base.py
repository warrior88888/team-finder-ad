from django import forms

from core.validators import check_github_url


class GithubUrlFormMixin(forms.Form):
    """Mixin that provides GitHub URL validation for any form."""

    def clean_github_url(self) -> str | None:
        url = self.cleaned_data.get("github_url")
        is_valid, error = check_github_url(url)
        if not is_valid:
            if error == "not_github":
                raise forms.ValidationError("Ссылка должна вести на GitHub")
            if error == "no_protocol":
                raise forms.ValidationError("Ссылка должна начинаться с https://")
        return url
