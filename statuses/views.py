from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomStatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    context_object_name = 'status'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(self.request, "Статус успешно удален")
            return redirect(success_url)
        except ProtectedError:
            messages.error(
                self.request, 
                "Невозможно удалить статус, потому что он используется"
            )
            return redirect('statuses')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = CustomStatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ID'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно изменен")
        return super().form_valid(form)