from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone

def index(request):
    tasks = Task.objects.all().order_by('completed', 'priority', 'deadline')
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'tasks/index.html', {'tasks': tasks, 'form': form, 'now': timezone.now()})

def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('index')

# API Views
from rest_framework import viewsets
from .serializers import taskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('completed', 'priority', 'deadline')
    serializer_class = taskSerializer