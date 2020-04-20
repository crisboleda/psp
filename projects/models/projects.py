
# Django
from django.db import models

# Models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100, help_text='Project name')
    description = models.CharField(max_length=250)
    is_finish = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField()
    planning_date = models.DateTimeField()

    users = models.ManyToManyField(User, related_name='project_users')

    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
