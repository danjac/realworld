from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("settings/", views.settings, name="settings"),
    path("check-email/", views.check_email, name="check_email"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("profile/follow/<int:user_id>/", views.follow, name="follow"),
]
