
# Django
from django.db import models

# Models
from django.contrib.auth.models import User


class PositionCompany(models.Model):
    name = models.CharField(max_length=100, help_text='Position inside a company', unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExperienceCompany(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='experencies_companies',
        help_text='User experencie'
    )
    
    name_company = models.CharField(max_length=70, help_text='Name company')

    position_company = models.ForeignKey(
        PositionCompany,
        on_delete=models.CASCADE,
        related_name='position_company',
        help_text='User position within a company'
    )

    years_position = models.IntegerField(default=0, help_text='Years occupying the position')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} was as {} in {} company".format(self.user, self.position_company, self.name_company)
    