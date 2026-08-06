"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from . import views as tasks_
from .api_views import SubTaskDetailUpdateDeleteView, SubTaskListCreateView

urlpatterns = [
    path('tasks/statistics/', tasks_.tasks_aggregate_all, name='tasks-statistics'),
    path('tasks/<uuid:pk>/', tasks_.tasks_requests, name='task-get-one-or-update-or-delete'),
    path('tasks/', tasks_.tasks_requests, name='task-get-all-or-create'),
    path('subtasks/<uuid:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-get-update-delete'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-get-all-or-create'),
    # path('tasks/count/', tasks_.tasks_count_all, name='task-count-all'),
    # path('tasks/status/<str:status_>', tasks_.tasks_by_status, name='task-count-by-status'),
    # path('tasks/expired/', tasks_.tasks_expired_date, name='task-expired-date')
]

