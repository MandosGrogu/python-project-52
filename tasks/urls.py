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
from django.urls import include, path

from tasks import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("", views.TaskListView.as_view(), name='tasks'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path(
        '<int:pk>/delete/', 
        views.TaskDeleteView.as_view(), 
        name='task_delete'
        ),
    path(
        '<int:pk>/update/', 
        views.TaskUpdateView.as_view(), 
        name='task_update'
        ),
    path('<int:pk>/', views.task_show_view, name='task_show'),
]
