
# Django
from django.views.generic import ListView, DetailView, FormView, TemplateView, UpdateView, RedirectView
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator

# Django REST Framework
from rest_framework.generics import UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

# Serializers
from programs.serializers import (UpdateBaseProgramSerializer, UpdateReusedPartSerializer, 
                                  EstimationModelSerializer, UpdateNewPartSerializer,
                                  NewPartModelSerializer)

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin
from programs.mixins import IsOwnerProgram
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from programs.models import Program, BasePart, ReusedPart, NewPart, Estimation, TypePart, SizeEstimation

# Forms 
from programs.forms import CreateBasePartForm, CreateReusedPartForm, CreateNewPartForm

# Utils
import json


class CreatePartProgramView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'parts_of_code/parts.html'

    def get_form_class(self):
        self.type_part = self.request.GET['type_part']
        if self.type_part and (self.type_part == 'base' or self.type_part == 'reused' or self.type_part == 'new'):
            if self.type_part == 'base':
                return CreateBasePartForm
            elif self.type_part == 'reused':
                return CreateReusedPartForm
            else:
                return CreateNewPartForm
        else:
            raise Http404("The URL doesn't valid")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'page' not in self.request.GET:
            self.page = 1
        else:
            self.page = self.request.GET['page']

        context["program_opened"] = self.program

        context["base_programs"] = Program.objects.exclude(pk=self.program.pk).filter(programmer=self.request.user)
        context["total_base_parts"] = BasePart.objects.filter(program=self.program).aggregate(total_planned_base_lines=Sum('lines_planned_base'), total_planned_deleted_lines=Sum('lines_planned_deleted'), total_planned_edited_lines=Sum('lines_planned_edited'), total_planned_added_lines=Sum('lines_planned_added'), total_current_base_lines=Sum('lines_current_base'), total_current_deleted_lines=Sum('lines_current_deleted'), total_current_edited_lines=Sum('lines_current_edited'), total_current_added_lines=Sum('lines_current_added'))

        # Context Base Parts
        context["base_parts"] = BasePart.objects.filter(program=self.program).order_by('created_at')

        # Context Reused parts
        context["reused_parts"] = ReusedPart.objects.filter(program=self.program).order_by('created_at')
        context["total_reused_parts"] = ReusedPart.objects.filter(program=self.program).aggregate(planning=Sum('planned_lines'), current=Sum('current_lines'))

        # Context New parts
        context["pagination_new_parts"] = Paginator(NewPart.objects.filter(program=self.program).order_by('created_at'), 5)
        context["new_parts"] = context["pagination_new_parts"].page(self.page)
        context["total_new_parts"] = NewPart.objects.filter(program=self.program).aggregate(planning=Sum('planning_lines'), current=Sum('current_lines'))

        context["type_parts"] = TypePart.objects.all()
        context["sizes_estimations"] = SizeEstimation.objects.all()

        serializer_estimations = EstimationModelSerializer(instance=Estimation.objects.all(), many=True)
        context["estimations"] = json.dumps(serializer_estimations.data, sort_keys=True)

        return context
    

    def form_valid(self, form):
        form.save(self.program)

        messages.success(self.request, "The {} part was created successfully".format(self.type_part))
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('programs:create_part_program', kwargs={'pk_program': self.program.pk}) + "?type_part={}".format(self.type_part)



class UpdateBaseProgramView(LoginRequiredMixin, UpdateAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = BasePart.objects.all()
    lookup_url_kwarg = 'pk_base_part'
    serializer_class = UpdateBaseProgramSerializer


class UpdateReusedPartView(LoginRequiredMixin, UpdateAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = ReusedPart.objects.all()
    lookup_url_kwarg = 'pk_reused_part'
    serializer_class = UpdateReusedPartSerializer


class UpdateNewPartView(LoginRequiredMixin, UpdateAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = NewPart.objects.all()
    lookup_url_kwarg = 'pk_new_part'
    serializer_class = UpdateNewPartSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_part = self.get_object()
            part = serializer.save(new_part)
            
            return Response(data=NewPartModelSerializer(instance=part).data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteReusedPartView(LoginRequiredMixin, DestroyAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = ReusedPart.objects.all()
    lookup_url_kwarg = 'pk_reused_part'
    serializer_class = UpdateReusedPartSerializer


class DeleteNewPartView(LoginRequiredMixin, DestroyAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = NewPart.objects.all()
    lookup_url_kwarg = 'pk_new_part'
    serializer_class = NewPartModelSerializer


class DeleteBasePartView(LoginRequiredMixin, DestroyAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = BasePart.objects.all()
    lookup_url_kwarg = 'pk_base_part'
    serializer_class = UpdateBaseProgramSerializer
