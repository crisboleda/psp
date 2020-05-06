
# Django
from django.urls import path

# Views
from projects.views import ListProjectView, CreateProjectView, DetailProjectView, UpdateProjectView, AddProgrammerProjectView, RemoveProgrammerProjectView

urlpatterns = [
    path('', ListProjectView.as_view(), name='list_projects'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('<int:pk>/preview/', DetailProjectView.as_view(), name='detail_project'),
    path('<int:pk>/update/', UpdateProjectView.as_view(), name='edit_project'),
    path('<int:pk_project>/add_programmer/', AddProgrammerProjectView.as_view(), name='add_programmer_to_project'),
    path('<int:pk_project>/remove_programmer/<str:username_programmer>/', RemoveProgrammerProjectView.as_view(), name='remove_programmer_to_project')
]
