from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Label
from django.contrib.auth.decorators import login_required
from .forms import CustomLabelForm
from django.db.models import ProtectedError

@login_required
def index(request):
    labels = Label.objects.all()
    return render(
        request,
        "labels.html",
        {'labels': labels},
    )

@login_required
@require_http_methods(['GET', 'POST'])
def label_create(request):
    if request.method == 'POST':
        form = CustomLabelForm(request.POST, request=request)
        if form.is_valid():
            label = form.save()
            messages.success(request, "Метка успешно создана")
            return redirect('labels') 
    else: 
        form = CustomLabelForm()
    return render(request, 'labels/create.html', {'form': form})

@login_required
@require_http_methods(['GET', 'POST'])
def label_delete_view(request, pk):
    label_obj = get_object_or_404(Label, pk=pk)
    try:
        label_obj.delete()
        messages.success(request, "Метка успешно удалена")
        return redirect('labels')
    except ProtectedError:
        messages.error(
            request, 
            "Невозможно удалить метку, потому что она используется"
        )
        return redirect('labels')

@login_required
@require_http_methods(['GET', 'POST'])
def label_update_view(request, pk):
    label_obj = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = CustomLabelForm(request.POST, instance=label_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Метка успешно изменена")
            return redirect('labels')
        else:
            form = CustomLabelForm()
            return render(request, 'labels/update.html', {'form': form, 'ID': pk})
    else:
        form = CustomLabelForm(instance=label_obj)
    return render(request, 'labels/update.html', {'form': form, 'ID': pk})