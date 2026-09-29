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

from labels import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("", views.LabelListView.as_view(), name='labels'),
    path('create/', views.LabelCreateView.as_view(), name='label_create'),
    path(
        '<int:pk>/delete/', 
        views.LabelDeleteView.as_view(), 
        name='label_delete'
        ),
    path(
        '<int:pk>/update/', 
        views.LabelUpdateView.as_view(), 
        name='label_update'
        ),
]
