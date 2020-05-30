from django.views.generic import TemplateView


class ReportView(TemplateView):
    template_name = 'test_report/reports.html'

class CreateReport(TemplateView):
    template_name = 'test_report/create_report.html'






