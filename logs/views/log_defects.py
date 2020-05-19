
# Django
from django.views.generic import ListView

# Models
from logs.models import DefectLog, DefectType

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin


class ListDefectLogView(MemberUserProgramRequiredMixin, ListView):
    template_name = 'defects/defects.html'
    context_object_name = 'log_defects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program 
        return context

    def get_queryset(self):
        return DefectLog.objects.filter(program=self.program)


class ListDefectTypeStandardView(MemberUserProgramRequiredMixin, ListView):
    queryset = DefectType.objects.all()
    template_name = 'defects/defect_type.html'
    context_object_name = 'type_defects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program
        return context
    
