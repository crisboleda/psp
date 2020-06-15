
# Django
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db.models import OuterRef, Sum, F, Subquery
from django.db.models.functions import Coalesce

# Models
from programs.models import BasePart, ReusedPart, Program

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Mixins
from users.mixins import UserExistMixin, AllowAccessUserPageMixin


class UserAnalysisToolsView(LoginRequiredMixin, UserExistMixin, AllowAccessUserPageMixin, APIView):

    def get(self, request, *args, **kwargs):

        base = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_base'))
        edited = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_edited'))
        deleted = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_deleted'))
        reused = ReusedPart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('current_lines'))

        actual_size = Program.objects.values('pk', 'name').filter(programmer=self.user).annotate(total=Coalesce((F('total_lines') - (Subquery(base.values('total')) - Subquery(deleted.values('total')) + Subquery(reused.values('total')) )) + Subquery(edited.values('total')), 0))

        data = {
            'actual_size': actual_size
        }

        return Response(data=data, status=status.HTTP_200_OK)