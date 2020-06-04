
# Django
from django.contrib import admin

# Models
from programs.models import ProgrammingLanguage, Estimation, SizeEstimation, TypePart, Report, Pip



@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'created_at', 'updated_at')
    search_fields = ('name',)



@admin.register(Estimation)
class EstimationNewPartAdmin(admin.ModelAdmin):
    list_display = ('type_part', 'size_estimation', 'lines_of_code', 'created_at', 'updated_at')
    list_filter = ('type_part', 'size_estimation')


@admin.register(SizeEstimation)
class SizeEstimationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', )


@admin.register(TypePart)
class TypePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Report)
class ListReports(admin.ModelAdmin):
    list_display =('program','name','date','objetive','description','conditions','expect_results','current_results')
    search_fields =('name',)

@admin.register(Pip)
class ListPip(admin.ModelAdmin):
    list_display=('program','name','date','problems','proposal','comment')
    search_fields = ('name',)

    