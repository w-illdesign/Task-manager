from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone

def index(request):
    tasks = Task.objects.all().order_by('completed', 'deadline')
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

import requests
def users(request):
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    api_users = response.json() if response.status_code == 200 else []

    return render(request, 'tasks/users.html', {
        'api_users': api_users,
    })

# API Views (if needed in the future)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import TaskSerializer

class TaskAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        categories = Task.objects.all()
        serializer = TaskSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)