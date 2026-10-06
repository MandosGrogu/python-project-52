from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CustomTaskForm, TaskFilterForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .select_related('status', 'author')
            .prefetch_related('labels')
        )

        self.filter_form = TaskFilterForm(self.request.GET or None)
        
        if self.filter_form.is_valid():
            cleaned_data = self.filter_form.cleaned_data
            
            if cleaned_data.get('label'):
                queryset = queryset.filter(labels=cleaned_data['label'])
                
            if cleaned_data.get('status'):
                queryset = queryset.filter(status=cleaned_data['status'])
                
            if cleaned_data.get('performer'):
                queryset = queryset.filter(performer=cleaned_data['performer'])
                
            if cleaned_data.get('only_my'):
                queryset = queryset.filter(author=self.request.user)
                
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filter_form
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        
        form.save_m2m()
        
        messages.success(self.request, "Задача успешно создана")
        return redirect(self.get_success_url())


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        task_obj = self.get_object()
        return task_obj.author == self.request.user

    def handle_no_permission(self):

        if self.request.user.is_authenticated:
            messages.warning(self.request, 
            "Задачу может удалить только ее автор")
            return redirect('tasks')

        return super().handle_no_permission()

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Задача успешно удалена")
        return redirect(success_url)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CustomTaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ID'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)