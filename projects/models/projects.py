
# Django
from django.db import models

# Models
from django.contrib.auth.models import User

# Estados que puede tener un proyecto
from projects.utils import CHOICES_STATUS_PROJECT

# Validators
from projects.validators import validate_min_length_description


class Project(models.Model):
    name = models.CharField(max_length=100, help_text='Project name')
    description = models.CharField(max_length=250, validators=[validate_min_length_description])

    status = models.CharField(
        max_length=15,
        choices=CHOICES_STATUS_PROJECT,
        default='En proceso',
        help_text='This atributte allows to save the project status'
    )
    
    start_date = models.DateField()
    finish_date = models.DateField(blank=True, null=True)
    planning_date = models.DateField()

    users = models.ManyToManyField(User, related_name='project_users')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_project')

    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
