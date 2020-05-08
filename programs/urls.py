
# Django
from django.urls import path

# Views
from programs.views import ProgramView

urlpatterns = [
    path('modules/<int:pk_module>/programs/', ProgramView.as_view(), name='list_programs')
]
