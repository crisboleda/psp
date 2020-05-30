
# Django
from django.urls import path

# Views
from programs.views import (AdminListProgramView, CreateProgramView, ProgrammerListProgramView,
                            DetailProgramView, CreatePartProgramView, UpdateBaseProgramView, 
                            UpdateReusedPartView, ListPIPView, ReportView, CreateReport)

urlpatterns = [
    path('modules/<int:pk_module>/programs/', AdminListProgramView.as_view(), name='list_programs'),
    path('modules/<int:pk_module>/programs/create/', CreateProgramView.as_view(), name='create_program'),
    path('programs/', ProgrammerListProgramView.as_view(), name='programs_programmer'),
    path('programs/<int:pk_program>/', DetailProgramView.as_view(), name='detail_program'),

    # PARTS OF CODE

    path('programs/<int:pk_program>/parts/', CreatePartProgramView.as_view(), name='create_part_program'),
    path('base_parts/<int:pk_base_part>/update/', UpdateBaseProgramView.as_view(), name='update_base_part'),
    path('reused_parts/<int:pk_reused_part>/update/', UpdateReusedPartView.as_view(), name='update_reused_part'),
    path('programs/<int:pk_>/pip/',ListPIPView.as_view(), name='List_pip_program'),
    path('programs/<int:pk_>/reports/', ReportView.as_view(), name='reports_view'),
    path('programs/<int:pk_>/create_reports/', CreateReport.as_view(), name='create_reports')


]
