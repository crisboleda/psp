
# Django
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

# Models
from logs.models import DefectLog, DefectType, Phase

# Forms
from logs.forms import CreateDefectLogForm

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin


class CreateDefectLogView(MemberUserProgramRequiredMixin, FormView):
    form_class = CreateDefectLogForm
    template_name = 'defects/defects.html'

    def form_valid(self, form):
        form.save(self.program)

        # Message defect created
        messages.success(self.request, "The defect was created successfully")
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program 
        context["phases"] = Phase.objects.all().order_by('order_index')
        context["type_defects"] = DefectType.objects.all().values('number', 'name')
        context["defect_logs"] = DefectLog.objects.filter(program=self.program)
        return context

    def get_success_url(self):
        return reverse_lazy('logs:program_defect_logs', kwargs={'pk_program': self.program.pk})


class ListDefectTypeStandardView(MemberUserProgramRequiredMixin, ListView):
    queryset = DefectType.objects.all()
    template_name = 'defects/defect_type.html'
    context_object_name = 'type_defects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program
        return context
    
