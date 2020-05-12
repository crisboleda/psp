
# Django
from django.contrib import admin

# Models
from logs.models import Phase, TimeLog

@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    fields = ('name', 'abbreviation', 'description')
    list_display = ('name', 'abbreviation', 'description')
