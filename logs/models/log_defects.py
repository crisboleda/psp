
# Django
from django.db import models

# Models
from programs.models import Program
from logs.models import Phase


class DefectType(models.Model):
    number = models.IntegerField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=20)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Type: {}  Name: {}".format(self.number, self.name)


class DefectLog(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='get_defects')
    defect = models.ForeignKey(DefectType, on_delete=models.CASCADE)
    date = models.DateTimeField()

    time_reparation = models.IntegerField(default=0)

    phase_injected = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_defect_found')
    phase_removed = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='phase_defect_removed')

    description = models.TextField(max_length=500)
    solution = models.TextField(max_length=500)

    cousing_defect = models.ForeignKey('DefectLog', null=True, on_delete=models.CASCADE, related_name='cousing_defect_defect')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} had defect {}".format(self.program, self.defect)
    
    
    
