
# Django
from django.urls import path

# Views
from programs.views import (AdminListProgramView, CreateProgramView, ProgrammerListProgramView,
                            DetailProgramView, TemplatePartsCodeView)

urlpatterns = [
    path('modules/<int:pk_module>/programs/', AdminListProgramView.as_view(), name='list_programs'),
    path('modules/<int:pk_module>/programs/create/', CreateProgramView.as_view(), name='create_program'),
    path('programs/', ProgrammerListProgramView.as_view(), name='programs_programmer'),
    path('programs/<int:pk_program>/', DetailProgramView.as_view(), name='detail_program'),

    path('programs/<int:pk_program>/parts_code/', TemplatePartsCodeView.as_view(), name='parts_of_code')
]
