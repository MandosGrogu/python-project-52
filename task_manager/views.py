from django.contrib import messages
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)

from .forms import UserCreationForm


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = "Вы залогинены"


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().post(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = "index.html"


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        referer = self.request.META.get('HTTP_REFERER', '')
        is_reg_url = 'signup' in referer
        
        context['from_reg'] = is_reg_url
        return context

    def form_valid(self, form):
        self.object = form.save()
        
        login(self.request, self.object)
        
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        
        return redirect(self.get_success_url())


User = get_user_model()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'registration/delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj

    def handle_no_permission(self):
        messages.warning(self.request, "У вас нет прав для изменения")
        return redirect('users')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Пользователь успешно удален")
        return redirect(success_url)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'registration/update.html'
    success_url = reverse_lazy('users')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj

    def handle_no_permission(self):
        messages.warning(self.request, "У вас нет прав для изменения")
        return redirect('users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        referer = self.request.META.get('HTTP_REFERER', '')
        is_reg_url = 'signup' in referer
        
        context['from_reg'] = is_reg_url
        context['ID'] = self.kwargs['pk']
        
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        update_session_auth_hash(self.request, self.object)
        
        messages.success(self.request, "Пользователь успешно изменен")
        return response