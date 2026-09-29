from django.contrib.auth import get_user_model
from django.db.models import Value
from django.db.models.functions import Concat
from django.views.generic import ListView

User = get_user_model()


class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'

    def get_queryset(self):
        return super().get_queryset().annotate(
            fullName=Concat('first_name', Value(' '), 'last_name')
        )