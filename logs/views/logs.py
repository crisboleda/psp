
# Django
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy

# Models
from logs.models import TimeLog, Phase

# Forms
from logs.forms import CreateLogProgramForm

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin


class ListProgramTimeLogView(MemberUserProgramRequiredMixin, ListView):
    template_name = 'logs/time_log.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return TimeLog.objects.filter(program=self.program)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program
        context["phases_not_in_program"] = Phase.objects.exclude(id__in=TimeLog.objects.filter(program=self.program)).values('name')
        return context


class CreateTimeLogView(FormView):
    form_class = CreateLogProgramForm
    success_url = reverse_lazy('programs:programs_programmer')

    def form_valid(self, form):
        form.save()
        super().form_valid(form)
    