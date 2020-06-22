
# Django
from django.db.models import Count, Q, F, Sum
from django.db.models.functions import Coalesce, Ceil
from django.http.response import Http404
from django.db import connection

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models
from logs.models import Phase, TimeLog
from programs.models import Program

# Permissions and Mixins
from programs.mixins import IsProgrammerProgram, ProgramExistMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class DataDefectInjectedView(LoginRequiredMixin, ProgramExistMixin, APIView):
    context = {
        "defects_injected": {},
        "defects_to_date": {}
    }

    def get(self, request, *args, **kwargs):

        self.context["defects_injected"] = Phase.objects.annotate(
            total=Count('name', filter=Q(phase_defect_found__program=self.program))
        ).values('name', 'total').order_by('order_index')

        self.context["defects_to_date"] = Phase.objects.annotate(
            total=Count('name', filter=Q(phase_defect_found__program__programmer=self.program.programmer))
        ).values('name', 'total').order_by('order_index')

        return Response(data=self.context, status=status.HTTP_200_OK)

    def get_permissions(self):
        return [IsProgrammerProgram(self.program)]


class DataTimePerPhaseView(LoginRequiredMixin, ProgramExistMixin, APIView):
    context = {
        "time_per_phase": {},
        "time_per_phase_to_date": {}
    }

    def get(self, request, *args, **kwargs):
        query_time_per_phase = "SELECT phase.name, COALESCE(CEIL(timelog.delta_time / 60.0), 0) AS total_time FROM logs_phase AS phase LEFT JOIN logs_timelog AS timelog ON (timelog.phase_id = phase.id AND timelog.program_id = {}) ORDER BY phase.order_index".format(self.program.pk)

        # Consulta con ORM Todavía no es apta para lo que se busca, se usa mientras (SQL PURO)
        '''query_time_per_phase = Phase.objects.annotate(total_time=Coalesce(Sum(Ceil(F('phase_log_time__delta_time') / 60.0), filter=Q(phase_log_time__program=self.program)), 0)).values('name', 'total_time').order_by('created_at')'''

        query_time_to_date = Phase.objects.annotate(total_time=Coalesce(Sum(Ceil(F('phase_log_time__delta_time') / 60.0), filter=Q(phase_log_time__program__programmer=self.program.programmer)), 0)).values('name', 'total_time').order_by('order_index')

        self.context["time_per_phase"] = self.my_custom_sql(query_time_per_phase)
        self.context["time_per_phase_to_date"] = query_time_to_date

        return Response(data=self.context, status=status.HTTP_200_OK)


    def my_custom_sql(self, query):
        with connection.cursor() as cursor:
            cursor.execute(query)
            return self.dictfetchall(cursor)


    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_permissions(self):
        return [IsProgrammerProgram(self.program)]



class DataDefectsRemovedView(LoginRequiredMixin, ProgramExistMixin, APIView):

    context = {
        "defects_removed": {},
        "defects_removed_to_date": {}
    }

    def get(self, request, *args, **kwargs):
    
        self.context["defects_removed"] = Phase.objects.annotate(
            total=Count('name', filter=Q(phase_defect_removed__program=self.program))
        ).values('name', 'total').order_by('order_index')

        self.context["defects_removed_to_date"] = Phase.objects.annotate(
            total=Count('name', filter=Q(phase_defect_removed__program__programmer=self.program.programmer))
        ).values('name', 'total').order_by('order_index')


        return Response(data=self.context, status=status.HTTP_200_OK)


    def get_permissions(self):
        return [IsProgrammerProgram(self.program)]

