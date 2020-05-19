
# Django
from django.contrib import admin

# Models
from logs.models import Phase, TimeLog, DefectType

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    fields = ('name', 'abbreviation', 'description')
    list_display = ('name', 'abbreviation', 'description')


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    fields = ('number', 'name', 'description')
    list_display = ('number', 'name', 'description', 'created_at', 'updated_at')