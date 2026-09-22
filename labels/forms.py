from django import forms
from django.utils.translation import pgettext_lazy

from .models import Label


class CustomLabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Label
        fields = ('title',)
    title = forms.CharField(
        label=pgettext_lazy("status label", "Title:"),
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
        if Label.objects.filter(title=title).exists() and self.request:
            raise forms.ValidationError("Label с таким Имя уже существует.")
        return title