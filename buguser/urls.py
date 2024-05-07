from django.urls import path, include
from .views import (
    SendPasswordResetEmailView,
    UserChangePasswordView,
    UserLoginView,
    UserProfileView,
    UserRegistrationView,
    UserPasswordResetView,
    UserDetails,
    UserProfilePic,
    UserTypes,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("changepassword/", UserChangePasswordView.as_view(), name="changepassword"),
    path(
        "send-reset-password-email/",
        SendPasswordResetEmailView.as_view(),
        name="send-reset-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="reset-password",
    ),
    path("sso/", include("allauth.urls")),
    path("user-details/", UserDetails.as_view(), name="user-details"),
    path("upload-profile-pic/", UserProfilePic.as_view(), name="upload-profile-pic"),
    path("usertypes/", UserTypes.as_view(), name="usertypes"),
]
