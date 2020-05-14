
# Django
from django.db import models
from django.utils import timezone

# Models
from programs.models import Program


class Phase(models.Model):
    name = models.CharField(max_length=50, help_text='Phase name')
    abbreviation = models.CharField(max_length=20)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TimeLog(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_log_time')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_log_time')

    comments = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    delta_time = models.IntegerField(default=0)
    finish_date = models.DateTimeField(null=True)

    last_restart_time = models.DateTimeField(auto_now_add=True)
    is_paused = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} in {}".format(self.program, self.phase)
    
    