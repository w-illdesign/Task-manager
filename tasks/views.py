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
from requests.exceptions import RequestException

def users(request):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/users', timeout=5)
        api_users = response.json() if response.status_code == 200 else []
        error = None
    except RequestException:
        api_users = []
        error = "Impossible de récupérer les utilisateurs externes. Veuillez vérifier votre connexion internet."

    return render(request, 'tasks/users.html', {
        'api_users': api_users,
        'error': error,
    })


from rest_framework import serializers, generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task

# ------------------------------
# SERIALIZER
# ------------------------------
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        """Vérifie que la date limite est bien renseignée."""
        if not value:
            raise serializers.ValidationError("La date limite (deadline) est obligatoire.")
        return value


# ------------------------------
# API BASÉE SUR LES VUES GÉNÉRIQUES
# ------------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    """Lister toutes les tâches ou en créer une nouvelle."""
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Afficher, modifier ou supprimer une tâche spécifique."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]


# ------------------------------
# API BASÉE SUR APIView (plus personnalisable)
# ------------------------------
from rest_framework.views import APIView

class TaskAPIView(APIView):
    """Vue personnalisée pour gérer les tâches."""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Liste toutes les tâches."""
        tasks = Task.objects.all().order_by('-id')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Crée une nouvelle tâche."""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Tâche créée avec succès ✅",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Erreur lors de la création ❌",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
