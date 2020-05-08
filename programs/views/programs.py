
# Django
from django.views.generic import TemplateView


class ProgramView(TemplateView):
    template_name = 'programs/programs.html'