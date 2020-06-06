# Django
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

# Django REST Framework
from rest_framework.generics import RetrieveDestroyAPIView

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin
from programs.mixins import IsOwnerProgram

# Serializers
from programs.serializers import PIPModelSerializer

# Models
from programs.models import Pip

# Mixins
from programs.mixins import OwnerReportPIPMixin

# Forms
from programs.forms import CreateListPip


class ListPIPView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'pip/pip.html'
    form_class = CreateListPip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program
        context["all_pip"] = Pip.objects.all().order_by('created_at')
        return context


    def get_success_url(self):
        return reverse_lazy('programs:list_pip_program', kwargs={'pk_program': self.program.pk})


    def form_valid(self, form):
        form.save(self.program)
        messages.success(self.request, "The PIP was created successfuly")
        return super().form_valid(form)


class UpdatePIPView(OwnerReportPIPMixin, UpdateView):
    queryset = Pip.objects.all()
    fields = ('name', 'date', 'problems', 'proposal', 'comment')
    pk_url_kwarg = 'pk_pip'
    template_name = 'pip/edit_pip.html'
    context_object_name = 'pip'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.get_object().program
        return context


    def get_success_url(self):
        return reverse_lazy('programs:list_pip_program', kwargs={'pk_program': self.get_object().program.pk})
    


class RetrieveDestroyPIPView(RetrieveDestroyAPIView):
    permission_classes = [IsOwnerProgram]
    queryset = Pip.objects.all()
    lookup_url_kwarg = 'pk_pip'
    serializer_class = PIPModelSerializer
