from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import User


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6)

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email.lower()


@require_POST
def login_or_signup(request: HttpRequest) -> JsonResponse:
    form = AuthForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        if not (user := authenticate(username=email, password=password)):
            if User.objects.filter(email=email).exists():
                return JsonResponse({"ok": False})

            user = User.objects.create_user(email, password)

        login(request, user)

        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False}, status=400)


@ensure_csrf_cookie
def csrf_token(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"csrftoken": csrf.get_token(request)})
