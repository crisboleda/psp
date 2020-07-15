
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db.models import OuterRef, Sum, F, Subquery, Q, Count
from django.db.models.functions import Coalesce, Ceil, NullIf

# Models
from programs.models import BasePart, ReusedPart, Program
from logs.models import Phase, TimeLog

# Utils Constants
from users.utils import TIME_TOTAL_BY_PROGRAM

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from users.serializers import DataProgramAnalysisTools

# Mixins
from users.mixins import UserExistMixin, AllowAccessUserPageMixin


class UserAnalysisToolsView(LoginRequiredMixin, UserExistMixin, AllowAccessUserPageMixin, APIView):

    data = {
        'actual_size': {},
        'defects_removed': {},
        'defects_injected': {},
        'total_time': {},
        'appraisal_COQ': {},
        'total_defects': {}
    }

    def get(self, request, *args, **kwargs):

        # -----> ACTUAL SIZE <-------
        base = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_base'))
        added = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_added'))
        deleted = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_deleted'))
        reused = ReusedPart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('current_lines'))

        self.data["actual_size"] = Program.objects.values('pk', 'name').filter(programmer=self.user, finish_date__isnull=False).annotate(total=Coalesce(Subquery(base.values('total')) - Subquery(deleted.values('total')) + Subquery(reused.values('total')) + Subquery(added.values('total')), 0))
        # -----> END ACTUAL SIZE <------

        # -----> Defects Removed <--------
        self.data["defects_removed"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(
            planning=Count('name', Q(get_defects__phase_removed__name='Planning')),
            design=Count('name', Q(get_defects__phase_removed__name='Design')),
            design_review=Count('name', Q(get_defects__phase_removed__name='Design Review')),
            codification=Count('name', Q(get_defects__phase_removed__name='Codification')),
            codification_review=Count('name', Q(get_defects__phase_removed__name='Codification Review')),
            compilation=Count('name', Q(get_defects__phase_removed__name='Compilation')),
            unit_test=Count('name', Q(get_defects__phase_removed__name='Unit Test')),
            postmortem=Count('name', Q(get_defects__phase_removed__name='Postmortem'))
        ).values('pk', 'name', 'planning', 'design', 'design_review', 'codification', 'codification_review', 'compilation', 'unit_test', 'postmortem').order_by('created_at')
        # -----> END Defects removed <------


        # -----> Defects Injected <-------
        self.data["defects_injected"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(
            planning=Count('name', Q(get_defects__phase_injected__name='Planning')),
            design=Count('name', Q(get_defects__phase_injected__name='Design')),
            design_review=Count('name', Q(get_defects__phase_injected__name='Design Review')),
            codification=Count('name', Q(get_defects__phase_injected__name='Codification')),
            codification_review=Count('name', Q(get_defects__phase_injected__name='Codification Review')),
            compilation=Count('name', Q(get_defects__phase_injected__name='Compilation')),
            unit_test=Count('name', Q(get_defects__phase_injected__name='Unit Test')),
            postmortem=Count('name', Q(get_defects__phase_injected__name='Postmortem'))
        ).values('pk', 'name', 'planning', 'design', 'design_review', 'codification', 'codification_review', 'compilation', 'unit_test', 'postmortem').order_by('created_at')
        # ------> END Defects injected <------

        # -----> Total time <--------
        self.data["total_time"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(total=TIME_TOTAL_BY_PROGRAM).values('pk', 'name', 'total').order_by('created_at')
        # -----> END total time <------

        # -----> Failure COQ <--------
        # Hago dos subconsultas que retornan el tiempo dedicado en la fase de compilación y de pruebas
        timelogComp = TimeLog.objects.filter(program__pk=OuterRef("pk"), phase__name='Compilation').annotate(time=Ceil(F('delta_time') / 60.0)).values('time')[:1]
        timelogUnit = TimeLog.objects.filter(program__pk=OuterRef("pk"), phase__name='Unit Test').annotate(time=Ceil(F('delta_time') / 60.0)).values('time')[:1]

        self.data["failure_COQ"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(total=Coalesce(100 * ((Coalesce(Subquery(timelogComp), 0) + Coalesce(Subquery(timelogUnit), 0)) / NullIf(TIME_TOTAL_BY_PROGRAM, 0)), 0)).values('pk', 'name', 'total').order_by('created_at')
        # ------> END Failure COQ <------

        # ------> Appraisal Cost Of Quality <---------
        # Hago dos subconsultas que retornan el tiempo dedicado en la fase de revisión de diseño y revisión de código
        timelog_design_review = TimeLog.objects.filter(program__pk=OuterRef("pk"), phase__name='Design Review').annotate(time=Ceil(F('delta_time') / 60.0)).values('time')[:1]
        timelog_code_review = TimeLog.objects.filter(program__pk=OuterRef("pk"), phase__name='Codification Review').annotate(time=Ceil(F('delta_time') / 60.0)).values('time')[:1]

        self.data["appraisal_COQ"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(total=Coalesce(100 * ((Coalesce(Subquery(timelog_design_review), 0) + Coalesce(Subquery(timelog_code_review), 0)) / NullIf(TIME_TOTAL_BY_PROGRAM, 0)), 0)).values('pk', 'name', 'total').order_by('created_at')
        # -------> END Total defects <-------

        # ------> Total defects <---------
        self.data["total_defects"] = Program.objects.filter(programmer=self.user, finish_date__isnull=False).annotate(total=Count('get_defects')).values('pk', 'name', 'total')
        # ------> END total defects <-------

        return Response(data=self.data, status=status.HTTP_200_OK)


class TestDataProgram(LoginRequiredMixin, UserExistMixin, AllowAccessUserPageMixin, APIView):

    def get(self, request, *args, **kwargs):
        return Response(data=DataProgramAnalysisTools(data=Program.objects.filter(programmer=self.user)).data, status=status.HTTP_200_OK)
