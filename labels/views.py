from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomLabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    context_object_name = 'label'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, "Метка успешно удалена")
            return redirect(success_url)
        except ProtectedError:
            messages.error(
                self.request, 
                "Невозможно удалить метку, потому что она используется"
            )
            return redirect('labels')


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = CustomLabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ID'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)