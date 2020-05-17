
# Django
from django.views.generic import TemplateView


class ListDefectLogView(TemplateView):
    template_name = 'defect_logs/defects.html'