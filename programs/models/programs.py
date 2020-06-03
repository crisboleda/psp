
# Django
from django.db import models

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage
from projects.models import Module

# Utils
from projects.validators import validate_min_length_description


class Program(models.Model):
    name = models.CharField(max_length=100, help_text='Program name')
    description = models.CharField(max_length=200, validators=[validate_min_length_description])
    programmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='program_user')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='program_language')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='program_module')

    planning_date = models.DateField()
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PIP(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='pip_program')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    problems = models.TextField()
    proposal = models.TextField()
    comment = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class REPORT(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='reports_view')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    problems = models.TextField()
    proposal = models.TextField()
    comment = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    



    