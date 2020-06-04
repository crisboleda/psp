# Django
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView
from django.urls import reverse_lazy

# Mixins
from psp.mixins import MemberUserProgramRequiredMixin

# Models
from programs.models import Pip

# Forms
from programs.forms import CreateListPip

class ListPIPView(MemberUserProgramRequiredMixin, FormView):
    template_name = 'programs/pip.html'
    form_class = CreateListPip


  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] =  self.program
        context["pip"] = Pip.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('programs:list_pip_program', kwargs={'pk_program': self.program.pk})


    def form_valid(self, form):
        form.save(self.program)
        return super().form_valid(form)
