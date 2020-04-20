
# Django
from django.db import models

# Models
from programs.models import Program


class Phase(models.Model):
    name = models.CharField(max_length=50, help_text='Phase name')
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TimeLog(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_log_time')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_log_time')

    commentaries = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    delta_time = models.TimeField()
    finish_date = models.DateTimeField()
    is_pause = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} in {}".format(self.program, self.phase)
    
    