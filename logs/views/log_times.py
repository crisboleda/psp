
# Django
from django.views.generic import ListView, FormView, DetailView
from django.http.response import JsonResponse
from django.http.response import Http404, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils import timezone

# Django REST Framework
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

# Logic
from logs.logic.convert_time import ConvertTime

# Serializers
from logs.serializers import UpdateTimeLogModelSerializer, TimeLogModelSerializer, CreateTimeLogModelSerializer

# Models
from logs.models import TimeLog, Phase
from programs.models import Program

# Forms
from logs.forms import CreateLogProgramForm

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin
from logs.mixins import IsUserOwnerProgram, TimeLogNotStop


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
        return context


class CreateTimeLogView(MemberUserProgramRequiredMixin, CreateAPIView):
    queryset = TimeLog.objects.all()
    serializer_class = CreateTimeLogModelSerializer
    
    def dispatch(self, request, *args, **kwargs):
        self.program = Program.objects.get(pk=kwargs['pk_program'])
        self.is_active_phase = self.program.program_log_time.filter(finish_date=None).exists()

        if self.is_active_phase:
            return HttpResponseBadRequest(reason='There is a phase active')

        return super().dispatch(request, *args, **kwargs)
    

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            time_log = serializer.save(self.program)
            return Response(data=TimeLogModelSerializer(instance=time_log).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pause time log
class UpdateCurrentTimeLog(UpdateAPIView):
    queryset = TimeLog.objects.all()
    permission_classes = [IsUserOwnerProgram, TimeLogNotStop]
    lookup_url_kwarg = 'pk_time_log'
    serializer_class = UpdateTimeLogModelSerializer


class StopCurrentTimeLogView(UpdateAPIView):
    queryset = TimeLog.objects.all()
    permission_classes = [IsUserOwnerProgram, TimeLogNotStop]
    lookup_url_kwarg = 'pk_time_log'
    serializer_class = UpdateTimeLogModelSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            data = serializer.validated_data
            time_log = self.get_object()

            time_log.delta_time = data['delta_time']
            time_log.is_paused = data['is_paused']
            time_log.finish_date = timezone.now()
            time_log.save()

            return Response(data=TimeLogModelSerializer(instance=time_log).data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Restart time log
class RestartTimeLog(APIView):
    permission_classes = [IsUserOwnerProgram, TimeLogNotStop]

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
        
        return Response(data=TimeLogModelSerializer(instance=self.time_log).data, status=status.HTTP_200_OK)


class DetailTimeLogView(MemberUserProgramRequiredMixin, DetailView):
    model = TimeLog
    template_name = 'logs/timer_time_log.html'
    context_object_name = 'time_log'

    def get_object(self):
        if self.program.program_log_time.filter(finish_date=None).exists():
            return self.program.program_log_time.get(finish_date=None)
        return None

        