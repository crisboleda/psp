# Django
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin

# Models
from programs.models import Report

# Forms
from programs.forms import CreateReportModelForm


class ReportView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'test_report/reports.html'
    form_class = CreateReportModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] =  self.program
        context["reports"] = Report.objects.all()
        return context


    def get_success_url(self):
        return reverse_lazy('programs:reports_view', kwargs={'pk_program': self.program.pk})


    def form_valid(self, form):
        form.save(self.program)
        return super().form_valid(form)




