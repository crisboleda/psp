
# Django
from django.contrib import admin

# Models
from users.models import PositionCompany, Profile


@admin.register(PositionCompany)
class PositionCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture', 'type_user', 'genere')
    search_fields = ('user', 'type_user')
    list_filter = ('type_user', 'genere')

