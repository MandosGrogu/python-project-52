from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CustomTaskForm, TaskFilterForm
from .models import Task


@login_required
def index(request):
    tasks = Task.objects.all()
    form = TaskFilterForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data.get('label'):
            tasks = tasks.filter(labels=form.cleaned_data['label'])

        if form.cleaned_data.get('status'):
            tasks = tasks.filter(status=form.cleaned_data['status'])
        
        if form.cleaned_data.get('performer'):
            tasks = tasks.filter(performer=form.cleaned_data['performer'])

        if form.cleaned_data.get('only_my') and request.user.is_authenticated:
            tasks = tasks.filter(author=request.user)
    return render(
        request,
        "tasks.html",
        {
        'tasks': tasks,
        'form': form
    },
    )


@login_required
@require_http_methods(['GET', 'POST'])
def task_create(request):
    if request.method == 'POST':
        form = CustomTaskForm(request.POST, request=request)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user 
            task.save()
            messages.success(request, "Задача успешно создана")
            return redirect('tasks') 
    else: 
        form = CustomTaskForm()
    return render(request, 'tasks/create.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def task_show_view(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/show.html', {'task': task_obj})


@login_required
@require_http_methods(['GET', 'POST'])
def task_delete_view(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    if task_obj.author != request.user:
        messages.warning(request, "Задачу может удалить только ее автор")
        return redirect('tasks')
    else:
        task_obj.delete()
        messages.success(request, "Задача успешно удалена")
        return redirect('tasks')


@login_required
@require_http_methods(['GET', 'POST'])
def task_update_view(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = CustomTaskForm(request.POST, instance=task_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Задача успешно изменена")
            return redirect('tasks')
        else:
            form = CustomTaskForm()
            return render(
                request, 
                'tasks/update.html', 
                {'form': form, 'ID': pk}
                )
    else:
        form = CustomTaskForm(instance=task_obj)
    return render(request, 'tasks/update.html', {'form': form, 'ID': pk})