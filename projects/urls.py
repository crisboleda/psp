
# Django
from django.urls import path

# Views
from projects.views import (ListProjectView, CreateProjectView, DetailProjectView, UpdateProjectView, 
                            AddProgrammerProjectView, RemoveProgrammerProjectView, ListModuleView,
                            CreateModuleView, UpdateModuleView)

urlpatterns = [

    # URLs CRUD Projects
    path('', ListProjectView.as_view(), name='list_projects'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('<int:pk_project>', DetailProjectView.as_view(), name='detail_project'),
    path('<int:pk_project>/update/', UpdateProjectView.as_view(), name='edit_project'),
    path('<int:pk_project>/add_programmer/', AddProgrammerProjectView.as_view(), name='add_programmer_to_project'),
    path('<int:pk_project>/remove_programmer/<str:username_programmer>/', RemoveProgrammerProjectView.as_view(), name='remove_programmer_to_project'),

    # URLs CRUD Modules
    path('<int:pk_project>/modules/', ListModuleView.as_view(), name='list_modules'),
    path('<int:pk_project>/modules/create/', CreateModuleView.as_view(), name='create_module'),
    path('<int:pk_project>/modules/<int:pk_module>/', UpdateModuleView.as_view(), name='update_module'),

]
