
# Django
from django.urls import path

# Views
from programs.views import ProgramView, CreateProgramView

urlpatterns = [
    path('modules/<int:pk_module>/programs/', ProgramView.as_view(), name='list_programs'),
    path('modules/<int:pk_module>/programs/create/', CreateProgramView.as_view(), name='create_program')
]
