from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
    search_fields = ['title', 'description']
    filterset_fields = ['completed']
    ordering_fields = ['title', 'created_at', 'completed']
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        return Response(self.get_serializer(task).data)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    search_query = request.GET.get('search', '').strip()
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | Q(
                description__icontains=search_query)
        )

    completed_filter = request.GET.get('completed')
    if completed_filter == 'true':
        tasks = tasks.filter(completed=True)
    elif completed_filter == 'false':
        tasks = tasks.filter(completed=False)

    sort_by = request.GET.get('sort', '-created_at')
    tasks = tasks.order_by(sort_by)

    context = {
        'tasks': tasks,
        'search_query': search_query,          # keep value in input
        'completed_filter': completed_filter,  # keep selected value
    }
    return render(request, 'task_list.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f'Task "{task_title}" deleted successfully.')
        return redirect('task_list')

    return redirect('task_list')


@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            Task.objects.create(user=request.user,
                                title=title, description=description)
    return redirect('task_list')


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')
