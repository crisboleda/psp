
# Django
from django.urls import path

# Views
from logs.views import (ListProgramTimeLogView, CreateTimeLogView, UpdateCurrentTimeLog, RestartTimeLog,
                        DetailTimeLogView, StopCurrentTimeLogView, ListDefectTypeStandardView,
                        CreateDefectLogView)


urlpatterns = [
    path('programs/<int:pk_program>/timelogs/', ListProgramTimeLogView.as_view(), name='program_time_logs'),
    path('programs/<int:pk_program>/timelogs/create/', CreateTimeLogView.as_view(), name='create_time_log'),

    path('timelogs/<int:pk_time_log>/pause/', UpdateCurrentTimeLog.as_view(), name='update_time_log'),
    path('timelogs/<int:pk_time_log>/restart/', RestartTimeLog.as_view(), name='restart_time_log'),
    path('timelogs/<int:pk_time_log>/stop/', StopCurrentTimeLogView.as_view(), name='stop_time_log'),

    path('programs/<int:pk_program>/timelogs/timer/', DetailTimeLogView.as_view(), name='current_time_log'),


    # URL LOG DEFECTS
    path('programs/<int:pk_program>/defect_logs/', CreateDefectLogView.as_view(), name='program_defect_logs'),


    # Type defects standard
    path('programs/<int:pk_program>/defects_type/', ListDefectTypeStandardView.as_view(), name='list_defects_type'),
]
