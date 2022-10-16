from django.urls import path

from . import views

urlpatterns = [
    path("login-or-signup/", views.login_or_signup, name="login-or-signup"),
    path("csrf-token/", views.csrf_token, name="csrf-token"),
]
