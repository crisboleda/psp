
# Django
from django.db import models

# Models
from programs.models import ProgrammingLanguage


class Algorithm(models.Model):
    name = models.CharField(max_length=100, help_text='Name algorithm')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Estimation(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='estimation_language')
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, related_name='estimation_algorithm')
    lines_of_code = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Algorithm '{}' in language {} are {} lines of code".format(self.algorithm, self.language, self.lines_of_code)
    