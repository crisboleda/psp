# Django
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin

# Models
from programs.models import REPORT

class ReportView(MemberUserProgramRequiredMixin, CreateView):
    template_name = 'test_report/reports.html'
    queryset = REPORT.objects.all()
    fields = ('description', 'problems', 'proposal', 'comment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] =  self.program
        return context








