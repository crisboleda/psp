
# Django
from django.db import models

# Models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100, help_text='Project name')
    description = models.CharField(max_length=250)
    
    choices_status_project = (('on_process', 'En progreso'), ('canceled', 'Cancelado'), ('paused', 'Pausado'), ('finished', 'Finalizado'))

    status = models.CharField(
        max_length=15,
        choices=choices_status_project,
        default='on_process',
        help_text='This atributte allows to save the project status'
    )
    
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    planning_date = models.DateTimeField()

    users = models.ManyToManyField(User, related_name='project_users')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_project')

    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
