from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status


class CustomStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Status
        fields = ('title',)
    title = forms.CharField(
        label=_("Title:"),
        widget=forms.TextInput(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
            )
        })
    )
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Status.objects.filter(title=title).exists() and self.request:
            raise forms.ValidationError(
                "Task status с таким Имя уже существует."
                )
        return title