from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("password/", views.PasswordChangeView.as_view(), name="password_change"),
]
