from django import forms
from django.contrib import messages
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    get_user_model,
)
from django.utils.translation import gettext_lazy as _

from users.models import User


class StyledLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("User Name:"),
        widget=forms.TextInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
            )
        })
    )
    password = forms.CharField(
        label=_("Password:"),
        widget=forms.PasswordInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                )
        })
    )


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = get_user_model() 
        fields = ("firstname", "lastname", "username", "password1", "password2")

    firstname = forms.CharField(required=False,
        label=_("First name:"),
        widget=forms.TextInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                )
        })
    )
    lastname = forms.CharField(required=False,
        label=_("Last name:"),
        widget=forms.TextInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                )
        })
    )
    username = forms.CharField(
        label=_("User Name:"),
        help_text=_(
            "Required field. Maximum 150 symbols. "
            "Only letters, numbers and symbols @/./+/-/_."
        ),
        widget=forms.TextInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                )
        })
    )
    password1 = forms.CharField(
        label=_("Password:"),
        help_text=_("Your password should contain at least 3 symbols."),
        widget=forms.PasswordInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'),
        })
    )
    password2 = forms.CharField(
        label=_("Confirm Password:"),
        help_text=_(
            "To confirm password, please, enter your password one more time."
            ),
        widget=forms.PasswordInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                ),
        })
    )

    field_order = [
        "firstname", 
        "lastname", 
        "username", 
        "password1", 
        "password2"
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Raise an error if they are present but do not match
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                "The two password fields do not match."
                )

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() \
        and self.request:
            messages.warning(self.request, "уже существует")
        return username