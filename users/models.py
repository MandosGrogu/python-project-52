from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

username_validator = RegexValidator(
    regex=r'^[a-zA-Zа-я-А-Я@\.\_+\-0-9]+$',
    message='This field can only contain letters, numbers and symbols @/./+/-/_.',
    code='invalid_username'
)

class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    username = models.CharField(max_length=150, validators=[username_validator], unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username