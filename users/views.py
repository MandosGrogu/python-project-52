from django.contrib.auth import get_user_model
from django.shortcuts import render


def index(request):
    users = get_user_model().objects.all()
    return render(
        request,
        "users.html",
        {'users': users},
    )