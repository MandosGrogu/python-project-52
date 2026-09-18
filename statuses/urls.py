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

from statuses import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("", views.index, name='statuses'),
    path('create/', views.status_create, name='status_create'),
    path('<int:pk>/delete/', views.status_delete_view, name='status_delete'),
    path('<int:pk>/update/', views.status_update_view, name='status_update'),
]
