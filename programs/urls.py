
# Django
from django.urls import path

# Views
from programs.views import (AdminListProgramView, CreateProgramView, ProgrammerListProgramView,
                            DetailProgramView, CreatePartProgramView, UpdateBaseProgramView, 
                            UpdateReusedPartView, ListPIPView, ReportView, 
                            UpdateNewPartView, DeleteReusedPartView, DeleteNewPartView,
                            DeleteBasePartView, ReportRetrieveDestroyView, UpdateReportView,
                            UpdatePIPView, RetrieveDestroyPIPView, DataDefectInjectedView,
                            DataTimePerPhaseView, DataDefectsRemovedView, ConfigurationProgramProgrammerView)


urlpatterns = [

    # Programs
    path('modules/<int:pk_module>/programs/', AdminListProgramView.as_view(), name='list_programs'),
    path('modules/<int:pk_module>/programs/create/', CreateProgramView.as_view(), name='create_program'),
    path('programs/', ProgrammerListProgramView.as_view(), name='programs_programmer'),
    path('programs/<int:pk_program>/', DetailProgramView.as_view(), name='detail_program'),
    path('programs/<int:pk_program>/settings/', ConfigurationProgramProgrammerView.as_view(), name='settings_program'),

    # PARTS OF CODE
    path('programs/<int:pk_program>/parts/', CreatePartProgramView.as_view(), name='create_part_program'),
    path('base_parts/<int:pk_base_part>/update/', UpdateBaseProgramView.as_view(), name='update_base_part'),
    path('reused_parts/<int:pk_reused_part>/update/', UpdateReusedPartView.as_view(), name='update_reused_part'),
    path('new_parts/<int:pk_new_part>/update/', UpdateNewPartView.as_view(), name='update_new_part'),
    path('reused_parts/<int:pk_reused_part>/delete/', DeleteReusedPartView.as_view(), name='delete_reused_part'),
    path('new_parts/<int:pk_new_part>/delete/', DeleteNewPartView.as_view(), name='delete_new_part'),
    path('base_parts/<int:pk_base_part>/delete/', DeleteBasePartView.as_view(), name='delete_base_part'),

    # PIP
    path('programs/<int:pk_program>/pip/', ListPIPView.as_view(), name='list_pip_program'),
    path('programs/<int:pk_program>/pip/<int:pk_pip>/', UpdatePIPView.as_view(), name='update_pip'),
    path('pips/<int:pk_pip>/', RetrieveDestroyPIPView.as_view(), name='pip_delete_detail'),

    # Reports
    path('programs/<int:pk_program>/reports/', ReportView.as_view(), name='reports_view'),
    path('programs/<int:pk_program>/reports/<int:pk_report>/', UpdateReportView.as_view(), name='update_report'),
    path('reports/<int:pk_report>/', ReportRetrieveDestroyView.as_view(), name='report_delete_detail'),

    # Summary
    path('programs/<int:pk_program>/data_defects_injected/', DataDefectInjectedView.as_view(), name='data_defects_injected'),
    path('programs/<int:pk_program>/data_time_per_phase/', DataTimePerPhaseView.as_view(), name='data_time_per_phase'),
    path('programs/<int:pk_program>/data_defects_removed/', DataDefectsRemovedView.as_view(), name='data_defects_removed'),
]
