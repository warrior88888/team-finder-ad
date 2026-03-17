from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from core.services.throttling import OverLimitError
from users import services
from users.forms import UserEditForm, UserLoginForm, UserRegisterForm
from users.types import UserRequest

from .mixins import UserMixin, UserSuccessUrlMixin


class UserDetailView(DetailView, UserMixin):
    template_name = "users/user-details.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.selector.user_details(user_pk=self.kwargs.get("pk"))


class UserListView(ListView, UserMixin):
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_authenticated:
            self.request: UserRequest
            return self.selector.participants_list(
                filter_by=self.request.GET.get("filter"),
                user=self.request.user,
            )
        return self.selector.participants_list()

    def get_context_data(self, **kwargs):
        """Проверка наличия условия для фильтрации в запросе"""
        context = super().get_context_data(**kwargs)
        context["active_filter"] = self.request.GET.get("filter")
        return context


class UserRegisterView(CreateView):
    """Logs the user in automatically after successful registration."""

    form_class = UserRegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        services.register_user(request=self.request, form=form)
        return redirect("projects:projects_list")


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def form_valid(self, form):
        try:
            services.login_user(
                request=self.request,
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"),
            )
            return redirect("projects:projects_list")
        except ValidationError:
            form.add_error(None, "Неверный имейл или пароль")
            return self.form_invalid(form)
        except OverLimitError:
            form.add_error(
                None,
                "Слишком много неудачных попыток! "
                "Попробуйте войти снова через 5 минут.",
            )
            return self.form_invalid(form)


class UserEditView(
    LoginRequiredMixin,
    UserSuccessUrlMixin,
    UpdateView,
    UserMixin,
):
    form_class = UserEditForm
    template_name = "users/edit_profile.html"
    request: UserRequest

    def form_valid(self, form: UserEditForm):
        services.edit_profile(request=self.request, form=form)
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(
    LoginRequiredMixin,
    UserSuccessUrlMixin,
    FormView,
):
    template_name = "users/change_password.html"
    form_class = PasswordChangeForm
    request: UserRequest

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        services.change_password(request=self.request, form=form)
        return redirect("users:user_detail", pk=self.request.user.pk)
