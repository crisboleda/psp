
# Django
from django.views.generic import ListView, FormView
from django.http.response import JsonResponse
from django.http.response import Http404, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils import timezone

# Django REST Framework
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Logic
from logs.logic.convert_time import ConvertTime

# Serializers
from logs.serializers import UpdateTimeLogModelSerializer

# Models
from logs.models import TimeLog, Phase
from programs.models import Program

# Forms
from logs.forms import CreateLogProgramForm

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin
from logs.mixins import IsUserOwnerProgram


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

        if context["is_active_phase"]:
            context["time_log"] = self.program.program_log_time.get(finish_date=None)
            context["total_time"] = ConvertTime.seconds_to_time(context['time_log'])
        return context


class CreateTimeLogView(MemberUserProgramRequiredMixin, FormView):
    form_class = CreateLogProgramForm

    def dispatch(self, request, *args, **kwargs):
        self.program = Program.objects.get(pk=kwargs['pk_program'])
        self.is_active_phase = self.program.program_log_time.filter(finish_date=None).exists()

        if self.is_active_phase:
            return HttpResponseBadRequest(reason='There is a phase active')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(self.program)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('logs:program_time_logs', kwargs={'pk_program': self.program.pk})



class UpdateCurrentTimeLog(UpdateAPIView):
    queryset = TimeLog.objects.all()
    permission_classes = [IsUserOwnerProgram]
    lookup_url_kwarg = 'pk_time_log'
    serializer_class = UpdateTimeLogModelSerializer


class RestartTimeLog(APIView):
    permission_classes = [IsUserOwnerProgram]

    def dispatch(self, request, *args, **kwargs):
        try:
            self.time_log = TimeLog.objects.get(pk=kwargs['pk_time_log'])
        except TimeLog.DoesNotExist:
            raise Http404("The time log doesn't exists")

        return super().dispatch(request, *args, **kwargs)

    def patch(self, request, pk_time_log):
        self.time_log.is_paused = False
        self.time_log.last_restart_time = timezone.now()
        self.time_log.save()
        
        return Response(data={'time_log_updated': 'yes'}, status=status.HTTP_200_OK)


    
