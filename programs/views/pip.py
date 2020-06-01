
# Django
from django.views.generic import TemplateView


class ListPIPView(TemplateView):
    template_name = 'programs/pip.html'

class PIPView(TemplateView):
    template_name = 'programs/pip_views.html'