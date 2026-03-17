from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("list/", views.UserListView.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("edit-profile/", views.UserEditView.as_view(), name="edit_profile"),
    path(
        "change-password/",
        views.UserPasswordChangeView.as_view(),
        name="change_password",
    ),
    path("logout/", views.user_logout, name="logout"),
    path("reset-avatar/", views.reset_user_avatar, name="reset_avatar"),
]
