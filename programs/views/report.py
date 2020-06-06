# Django
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

# Mixins and Permissions
from psp.mixins import MemberUserProgramRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from programs.mixins import IsOwnerProgram, OwnerReportPIPMixin

# Django REST Framework
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView

# Models
from programs.models import Report

# Serializers
from programs.serializers import ReportModelSerializer

# Forms
from programs.forms import CreateReportModelForm


class ReportView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'test_report/reports.html'
    form_class = CreateReportModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] =  self.program
        context["reports"] = Report.objects.all().order_by('created_at')
        return context


    def get_success_url(self):
        return reverse_lazy('programs:reports_view', kwargs={'pk_program': self.program.pk})


    def form_valid(self, form):
        form.save(self.program)
        messages.success(self.request, "The report was created successfuly")

        return super().form_valid(form)



class ReportRetrieveDestroyView(LoginRequiredMixin, RetrieveDestroyAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = Report.objects.all()
    lookup_url_kwarg = 'pk_report'
    serializer_class = ReportModelSerializer


class UpdateReportView(OwnerReportPIPMixin, UpdateView):
    queryset = Report.objects.all()
    template_name = 'test_report/update_report.html'
    pk_url_kwarg = 'pk_report'
    context_object_name = 'report'
    fields = ('name', 'date', 'objetive', 'description', 'conditions', 'expect_results', 'current_results')

    def get_success_url(self):
        messages.info(self.request, "The report was updated successfuly")
        return reverse_lazy('programs:reports_view', kwargs={'pk_program': self.get_object().program.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.get_object().program 
        return context
    