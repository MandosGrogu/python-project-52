from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CustomStatusForm
from .models import Status


@login_required
def index(request):
    statuses = Status.objects.all()
    return render(
        request,
        "statuses.html",
        {'statuses': statuses},
    )


@login_required
@require_http_methods(['GET', 'POST'])
def status_create(request):
    if request.method == 'POST':
        form = CustomStatusForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно создан")
            return redirect('statuses') 
    else: 
        form = CustomStatusForm()
    return render(request, 'statuses/create.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def status_delete_view(request, pk):
    status_obj = get_object_or_404(Status, pk=pk)
    try:
        if request.method == 'POST':
            status_obj.delete()
            messages.success(request, "Статус успешно удален")
            return redirect('statuses')
        else:
            return render(request, 'statuses/delete.html', {
        'status': status_obj
        })
    except ProtectedError:
        messages.error(
            request, 
            "Невозможно удалить статус, потому что он используется"
        )
        return redirect('statuses')


@login_required
@require_http_methods(['GET', 'POST'])
def status_update_view(request, pk):
    status_obj = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = CustomStatusForm(request.POST, instance=status_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно изменен")
            return redirect('statuses')
        else:
            form = CustomStatusForm()
            return render(
                request, 
                'statuses/update.html', 
                {'form': form, 'ID': pk}
                )
    else:
        form = CustomStatusForm(instance=status_obj)
    return render(request, 'statuses/update.html', {'form': form, 'ID': pk})