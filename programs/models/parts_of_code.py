
# Django
from django.db import models

# Models
from programs.models import Program, ProgrammingLanguage


class ReusedPart(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_reused_part')
    program_reused_part = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='reused_part')

    planned_lines = models.IntegerField(default=0)
    current_lines = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "Planned lines: {} - Current lines: {}".format(self.planned_lines, self.current_lines)


class BasePart(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_base_part')
    program_base = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='base_part')

    lines_planned_base = models.IntegerField(default=0)
    lines_planned_deleted = models.IntegerField(default=0)
    lines_planned_edited = models.IntegerField(default=0)
    lines_planned_added = models.IntegerField(default=0)

    lines_current_base = models.IntegerField(null=True)
    lines_current_deleted = models.IntegerField(null=True)
    lines_current_edited = models.IntegerField(null=True)
    lines_current_added = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Program '{}' has as base program '{}'".format(self.program, self.program_base)


class SizePart(models.Model):
    name = models.CharField(max_length=50, help_text='Size new part')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class NewPart(models.Model):
    name = models.CharField(max_length=150)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='new_part_program')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='new_part_language')

    planning_lines = models.IntegerField()
    planning_methods = models.IntegerField()
    planning_size = models.ForeignKey(SizePart, on_delete=models.CASCADE, related_name='planning_size_new_part')

    current_lines = models.IntegerField()
    current_methods = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    
    