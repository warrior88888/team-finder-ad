from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from users.forms import UserEditForm

User = get_user_model()


class AdminUserChangeForm(UserEditForm):
    password = ReadOnlyPasswordHashField(label=_("Password"))

    class Meta(UserEditForm.Meta):
        model = User
        fields = (
            *UserEditForm.Meta.fields,
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

    def clean_password(self):
        return self.initial.get("password")
