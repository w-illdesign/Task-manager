from django.contrib import admin
from django.urls import path, include
from tasks import views
from tasks.views import (
    TaskAPIView,
    TaskListCreateView,
    TaskRetrieveUpdateDeleteView
)

urlpatterns = [
    # ------------------------------
    # ADMINISTRATION
    # ------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------
    # APPLICATION PRINCIPALE
    # ------------------------------
    path('', views.index, name='index'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('users/', views.users, name='users'),

    # ------------------------------
    # API DJANGO REST FRAMEWORK
    # ------------------------------
    path('api-auth/', include('rest_framework.urls')),

    # Endpoints REST principaux
    path('api/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='task-detail'),

    # Endpoint API personnalisé
    path('api/tasks/custom/', TaskAPIView.as_view(), name='task-api-custom'),
]
