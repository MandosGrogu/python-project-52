from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.auth import get_user_model
from django.shortcuts import render


def index(request):
    users = get_user_model().objects.annotate(
    fullname=Concat('first_name', Value(' '), 'last_name')
)
    return render(
        request,
        "users.html",
        {'users': users},
    )