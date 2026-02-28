from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    task_list_page,
    complete_task,
)

urlpatterns = [

    path('', TaskListCreateView.as_view(), name='task_list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('complete/<int:pk>/', complete_task, name='complete_task'),
    path('page/', task_list_page, name='task_list_page'),
]
