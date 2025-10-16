from django.contrib import admin
from django.urls import path, include
from tasks import views
from tasks.views import TaskAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', views.index, name='index'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('users/', views.users, name='users'),

    # API URLs
    path('api-auth/', include('rest_framework.urls')),
    path('api/', TaskAPIView.as_view()),
]