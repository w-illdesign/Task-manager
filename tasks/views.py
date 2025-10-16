from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone

def index(request):
    # tri simple : d'abord non complétées (false) puis priorité (H,M,L) puis deadline asc
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

