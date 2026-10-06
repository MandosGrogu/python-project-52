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
from django.urls import include, path

from labels import views as labels_views
from statuses import views as statuses_views
from task_manager import views
from tasks import views as tasks_views
from users import views as users_views

from .forms import StyledLoginForm
from .views import (
    CustomLoginView,
    CustomLogoutView,
    IndexView,
    SignUpView,
    UserDeleteView,
    UserUpdateView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path("", IndexView.as_view(), name='index'),
    path(
        'login/', 
        CustomLoginView.as_view(form_class=StyledLoginForm), 
        name='login'
        ),
    path('users/create/', SignUpView.as_view(), name='signup'),
    path('users/', users_views.UserListView.as_view(), name="users"),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path(
        'statuses/', 
        statuses_views.StatusListView.as_view(), 
        name='statuses'
        ),
    path(
        'statuses/create/', 
        statuses_views.StatusCreateView.as_view(), 
        name='status_create'
        ),
    path(
        'statuses/<int:pk>/delete/', 
        statuses_views.StatusDeleteView.as_view(), 
        name='status_delete'
        ),
    path(
        'statuses/<int:pk>/update/', 
        statuses_views.StatusUpdateView.as_view(), 
        name='status_update'
        ),
    path("tasks/", tasks_views.TaskListView.as_view(), name='tasks'),
    path(
        'tasks/create/', 
        tasks_views.TaskCreateView.as_view(), 
        name='task_create'
        ),
    path(
        'tasks/<int:pk>/delete/', 
        tasks_views.TaskDeleteView.as_view(), 
        name='task_delete'
        ),
    path(
        'tasks/<int:pk>/update/', 
        tasks_views.TaskUpdateView.as_view(), 
        name='task_update'
        ),
    path(
        'tasks/<int:pk>/', 
        tasks_views.TaskDetailView.as_view(), 
        name='task_show'
        ),
    path("labels/", labels_views.LabelListView.as_view(), name='labels'),
    path(
        'labels/create/', 
        labels_views.LabelCreateView.as_view(), 
        name='label_create'
        ),
    path(
        'labels/<int:pk>/delete/', 
        labels_views.LabelDeleteView.as_view(), 
        name='label_delete'
        ),
    path(
        'labels/<int:pk>/update/', 
        labels_views.LabelUpdateView.as_view(), 
        name='label_update'
        ),
]
