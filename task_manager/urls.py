"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from task_manager import views
from .forms import StyledLoginForm
from .views import CustomLoginView, CustomLogoutView
from users import urls as users_urls
from statuses import urls as statuses_urls
from statuses import views as statuses_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("", views.index, name='index'),
    path('login/', CustomLoginView.as_view(form_class=StyledLoginForm), name='login'),
    path('users/create/', views.signup_view, name='signup'),
    path('users/', include(users_urls), name="users"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/<int:pk>/delete/', views.delete_view, name='delete'),
    path('users/<int:pk>/update/', views.update_view, name='update'),
    path('statuses/', include(statuses_urls), name='statuses'),
    path('statuses/create/', statuses_views.status_create, name='status_create'),
    path('statuses/<int:pk>/delete/', statuses_views.status_delete_view, name='status_delete'),
    path('statuses/<int:pk>/update/', statuses_views.status_update_view, name='status_update'),
]
