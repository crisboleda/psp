
# Django
from django.db import models

# Models
from programs.models import Program
from logs.models import Phase


class DefectType(models.Model):
    _type = models.CharField(max_length=55)
    name = models.CharField(max_length=20)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Type: {}  Name: {}".format(self._type, self.name)


class DefectLog(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    defect = models.ForeignKey(DefectType, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    time_reparation = models.TimeField()

    phase_found = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_defect_found')
    phase_removed = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_defect_removed')

    description = models.TextField()
    solution = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)

    # TODO Queda pendiente ver los defectos en cadena anteriormente

    def __str__(self):
        return "{} had defect {}".format(self.program, self.defect)
    
    
    
