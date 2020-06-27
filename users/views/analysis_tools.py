
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db.models import OuterRef, Sum, F, Subquery, Q, Count
from django.db.models.functions import Coalesce

# Models
from programs.models import BasePart, ReusedPart, Program
from logs.models import Phase

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
        'defects_injected': {}
    }

    def get(self, request, *args, **kwargs):

        # -----> ACTUAL SIZE <-------
        base = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_base'))
        edited = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_edited'))
        deleted = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_deleted'))
        reused = ReusedPart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('current_lines'))

        self.data["actual_size"] = Program.objects.values('pk', 'name').filter(programmer=self.user).annotate(total=Coalesce((F('total_lines') - (Subquery(base.values('total')) - Subquery(deleted.values('total')) + Subquery(reused.values('total')) )) + Subquery(edited.values('total')), 0))
        # -----> END ACTUAL SIZE <------

        # -----> Defects Removed <--------
        self.data["defects_removed"] = Program.objects.filter(programmer=self.user).annotate(
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
        self.data["defects_injected"] = Program.objects.filter(programmer=self.user).annotate(
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

        return Response(data=self.data, status=status.HTTP_200_OK)


class TestDataProgram(LoginRequiredMixin, UserExistMixin, AllowAccessUserPageMixin, APIView):

    def get(self, request, *args, **kwargs):
        return Response(data=DataProgramAnalysisTools(data=Program.objects.filter(programmer=self.user)).data, status=status.HTTP_200_OK)
