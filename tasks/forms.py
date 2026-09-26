from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from labels.models import Label
from statuses.models import Status
from users.models import User

from .models import Task


class CustomTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['performer'].label_from_instance = lambda obj: \
        f"{obj.first_name} {obj.last_name}".strip() or obj.username
        
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'performer', 'labels')
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
    description = forms.CharField(
        label=_("Description:"),
        widget=forms.Textarea(attrs={
            'class': (
                'block w-full border-2 border-gray-300 outline-none '
                'focus:outline-none focus:ring-1 focus:ring-blue-700 '
                'focus:border-blue-700 py-2 text-lg form-control'
                )
        })
    )
    status = forms.ModelChoiceField(
        label=_("Status:"),
        queryset=Status.objects.all(),
        empty_label="Choose status",
        widget=forms.Select(attrs={'class': (
            'block w-full border-2 border-gray-300 outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    performer = forms.ModelChoiceField(
        label=_("Performer:"),
        queryset=User.objects.all(),
        empty_label="Choose performer",
        required=False,
        widget=forms.Select(attrs={'class': (
            'block w-full border-2 border-gray-300 outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    labels = forms.ModelMultipleChoiceField(
      queryset=Label.objects.all(),
      widget=forms.SelectMultiple(attrs={'class': (
        'block w-full border-2 border-gray-300 outline-none '
        'focus:outline-none focus:ring-1 focus:ring-blue-700 '
        'focus:border-blue-700 py-2 text-lg form-control'
        )}),
      label=_('Labels:'),
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exists() and self.request:
            raise forms.ValidationError("Task с таким Имя уже существует.")
        return title


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        empty_label="Не выбрано",
        required=False,
        label=_("Status"),
        widget=forms.Select(attrs={'class': (
            'block w-full border-2 border-gray-300 bg-white outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_("Label"),
        empty_label="Не выбрано",
        widget=forms.Select(attrs={'class': (
            'block w-full border-2 border-gray-300 bg-white outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    performer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Не выбрано",
        required=False,
        label=_("Performer"),
        widget=forms.Select(attrs={'class': (
            'block w-full border-2 border-gray-300 bg-white outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    only_my = forms.BooleanField(
        required=False, 
        label=_("Only own tasks:"),
        widget=forms.CheckboxInput(attrs={'class': (
            'block w-full border-2 border-gray-300 bg-white outline-none '
            'focus:outline-none focus:ring-1 focus:ring-blue-700 '
            'focus:border-blue-700 py-2 text-lg form-control'
            )})
    )
    field_order = ['status', 'performer', 'label', 'only_my']

    def clean(self):
        cleaned_data = super().clean()
        for field_name, vl in list(cleaned_data.items()):
            if isinstance(vl, list):
                cleaned_data[field_name] = [v for v in vl if v != 'Не выбрано']

        return cleaned_data