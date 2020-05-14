
# Django
from django.urls import path

# Views
from logs.views import ListProgramTimeLogView, CreateTimeLogView, UpdateCurrentTimeLog, RestartTimeLog


urlpatterns = [
    path('programs/<int:pk_program>/timelogs/', ListProgramTimeLogView.as_view(), name='program_time_logs'),
    path('programs/<int:pk_program>/timelogs/create/', CreateTimeLogView.as_view(), name='create_time_log'),

    path('timelogs/<int:pk_time_log>/pause/', UpdateCurrentTimeLog.as_view(), name='update_time_log'),
    path('timelogs/<int:pk_time_log>/restart/', RestartTimeLog.as_view(), name='restart_time_log'),
]
