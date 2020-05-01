
# Django
from django.views.generic import TemplateView


class ListProjectView(TemplateView):
    template_name = 'projects/projects.html'