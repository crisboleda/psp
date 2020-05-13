
# Django
from django.views.generic import ListView, FormView
from django.http.response import JsonResponse
from django.http.response import Http404
from django.urls import reverse_lazy

# Models
from logs.models import TimeLog, Phase
from programs.models import Program

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
        context["phases_not_in_program"] = Phase.objects.exclude(id__in=TimeLog.objects.filter(program=self.program).values('phase__pk')).values('name')
        context["is_active_phase"] = self.program.program_log_time.filter(finish_date=None).exists()
        context["time_log"] = self.program.program_log_time.get(finish_date=None)
        return context


class CreateTimeLogView(MemberUserProgramRequiredMixin, FormView):
    form_class = CreateLogProgramForm

    def dispatch(self, request, *args, **kwargs):
        self.program = Program.objects.get(pk=kwargs['pk_program'])
        self.is_active_phase = self.program.program_log_time.filter(finish_date=None).exists()

        if self.is_active_phase:
            raise Http404("There is a phase active")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(self.program)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('logs:create_time_log', kwargs={'pk_program': self.program.pk})



def update_time_log(request, pk_time_log):
    print(request)
    import pdb; pdb.set_trace()
