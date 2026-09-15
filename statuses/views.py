from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Status
from django.contrib.auth.decorators import login_required
from .forms import CustomStatusForm

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
            status = form.save()
            messages.success(request, "Статус успешно создан")
            return redirect('statuses') 
        else:
            form = CustomStatusForm()
        return render(request, 'statuses/create.html', {'form': form})
    else: 
        form = CustomStatusForm()
    return render(request, 'statuses/create.html', {'form': form})

@login_required
@require_http_methods(['GET', 'POST'])
def status_delete_view(request, pk):
    status_obj = get_object_or_404(Status, pk=pk)
    status_obj.delete()
    messages.success(request, "Статус успешно удален")
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
            return render(request, 'statuses/update.html', {'form': form, 'ID': pk})
    else:
        form = CustomStatusForm(instance=status_obj)
    return render(request, 'statuses/update.html', {'form': form, 'ID': pk})