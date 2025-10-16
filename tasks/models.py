from django.db import models
from django.db import models

class Task(models.Model):
    PRIORITY_HIGH = 'H'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_LOW = 'L'
    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, 'Haute'),
        (PRIORITY_MEDIUM, 'Moyenne'),
        (PRIORITY_LOW, 'Basse'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)

    def __str__(self):
        return self.title
        
