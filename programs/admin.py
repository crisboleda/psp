
# Django
from django.contrib import admin

# Models
from programs.models import ProgrammingLanguage


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'created_at', 'updated_at')
    search_fields = ('name',)
