
# Django
from django.urls import path

# Views
from projects.views import ListProjectView

urlpatterns = [
    path('', ListProjectView.as_view(), name='list_projects'),
]
