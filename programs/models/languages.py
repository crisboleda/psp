
# Django
from django.db import models


# Model Programming Language 
class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True, help_text='Programming language name')
    picture = models.ImageField(upload_to='languages/', help_text='Programming language image')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    