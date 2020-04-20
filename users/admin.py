
# Django
from django.contrib import admin

# Models
from users.models import PositionCompany


@admin.register(PositionCompany)
class PositionCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
