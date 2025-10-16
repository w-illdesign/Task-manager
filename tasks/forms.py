from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Ajouter une tâche...',
                'autocomplete': 'off',
            }),

            'description': forms.TextInput(attrs={
                'placeholder': 'Ajouter une description...',
                'autocomplete': 'off',
            }),
            

            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            }),
            'priority': forms.Select(attrs={
                'aria-label': 'Priorité'
            }),
        }