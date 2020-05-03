
# Django
from django.urls import path

# Views
from projects.views import ListProjectView, CreateProjectView

urlpatterns = [
    path('', ListProjectView.as_view(), name='list_projects'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
]
