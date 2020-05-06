
# Django
from django.db import models

# Models
from django.contrib.auth.models import User

# Estados que puede tener un proyecto
from projects.utils import CHOICES_STATUS_PROJECT


class Project(models.Model):
    name = models.CharField(max_length=100, help_text='Project name')
    description = models.CharField(max_length=250)

    status = models.CharField(
        max_length=15,
        choices=CHOICES_STATUS_PROJECT,
        default='En proceso',
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
    
