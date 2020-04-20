
# Django
from django.db import models

# Models
from projects.models import Project


class Module(models.Model):
    name = models.CharField(max_length=100, help_text='Module name')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='modules')
    description = models.CharField(max_length=200, help_text='Module description')

    planning_date = models.DateField()
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
