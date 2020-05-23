
# Django
from django.views.generic import TemplateView

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin


class TemplatePartsCodeView(MemberUserProgramRequiredMixin, TemplateView):
    template_name = 'parts_of_code/parts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program 
        return context

    