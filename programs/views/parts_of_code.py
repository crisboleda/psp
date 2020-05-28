
# Django
from django.views.generic import ListView, DetailView, FormView, TemplateView, UpdateView, RedirectView
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages

# Django REST Framework
from rest_framework.generics import UpdateAPIView

# Serializers
from programs.serializers import UpdateBaseProgramSerializer, UpdateReusedPartSerializer

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin
from programs.mixins import IsOwnerProgram
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from programs.models import Program, BasePart, ReusedPart, NewPart

# Models 
from programs.forms import CreateBasePartForm, CreateReusedPartForm

    

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
            raise Http404("The URL doesn't valid")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["program_opened"] = self.program
        context["base_programs"] = Program.objects.exclude(pk=self.program.pk).filter(programmer=self.request.user)

        context["base_parts"] = BasePart.objects.filter(program=self.program)
        context["reused_parts"] = ReusedPart.objects.filter(program=self.program)
        context["new_parts"] = NewPart.objects.filter(program=self.program)

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

