from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model


def index(request):
    users = get_user_model().objects.all()
    return render(
        request,
        "users.html",
        {'users': users},
    )