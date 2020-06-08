
# Django
from django.db.models import Count, Q
from django.http.response import Http404

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Models
from logs.models import Phase
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
        ).values('name', 'total').order_by('created_at')

        self.context["defects_to_date"] = Phase.objects.annotate(
            total=Count('name', filter=Q(phase_defect_found__program__programmer=self.program.programmer))
        ).values('name', 'total').order_by('created_at')

        return Response(data=self.context, status=status.HTTP_200_OK)

    def get_permissions(self):
        return [IsProgrammerProgram(self.program)]