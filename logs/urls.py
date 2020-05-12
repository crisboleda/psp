
# Django
from django.urls import path

# Views
from logs.views import ListProgramTimeLogView, CreateTimeLogView


urlpatterns = [
    path('programs/<int:pk_program>/timelogs/', ListProgramTimeLogView.as_view(), name='program_time_logs'),
    path('programs/<int:pk_program>/timelogs/create/', CreateTimeLogView.as_view(), name='create_time_log'),
]
