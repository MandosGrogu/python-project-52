from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import UserCreationForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = "Вы залогинены"


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().post(request, *args, **kwargs)


def index(request):
    return render(
        request,
        "index.html",
    )


@require_http_methods(['GET', 'POST'])
def signup_view(request):
    referer = request.META.get('HTTP_REFERER', '')
    
    is_reg_url = False

    if 'signup' in referer:
        is_reg_url = True
        
    context = {
        'from_reg': is_reg_url,
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request=request)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            messages.success(request, "Пользователь успешно зарегистрирован")
            return redirect('login') 
    form = UserCreationForm()
    context['form'] = form
    return render(request, 'registration/signup.html', context)


@require_http_methods(['GET', 'POST'])
def delete_view(request, pk):
    User = get_user_model()
    user_obj = get_object_or_404(User, pk=pk)
    if request.user != user_obj:
        messages.warning(request, "У вас нет прав для изменения")
        return redirect('users')
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "Пользователь успешно удален")
    return redirect('users')


@require_http_methods(['GET', 'POST'])
def update_view(request, pk):
    referer = request.META.get('HTTP_REFERER', '')
    
    is_reg_url = False

    if 'signup' in referer:
        is_reg_url = True
        
    context = {
        'from_reg': is_reg_url,
        'ID': pk
    }

    User = get_user_model()
    user_obj = get_object_or_404(User, pk=pk)
    if request.user != user_obj:
        messages.warning(request, "У вас нет прав для изменения")
        return redirect('users')
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно изменен")
            return redirect('users')
        else:
            form = UserCreationForm()
            context['form'] = form
            return render(request, 'registration/update.html', context)
    else:
        form = UserCreationForm(instance=user_obj)
        context['form'] = form
    return render(request, 'registration/update.html', context)