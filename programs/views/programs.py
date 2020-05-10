
# Django
from django.views.generic import ListView, FormView
from django.http.response import Http404
from django.urls import reverse_lazy

# Models
from programs.models import Program, ProgrammingLanguage
from projects.models import Module

# Forms
from programs.forms import CreateProgramForm

# Mixins
from psp.mixins import AdminRequiredMixin


class ProgramView(ListView):
    queryset = Program.objects.all()
    template_name = 'programs/programs.html'
    context_object_name = 'programs'


class CreateProgramView(AdminRequiredMixin, FormView):
    template_name = 'programs/create_program.html'
    form_class = CreateProgramForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.module = Module.objects.get(pk=self.kwargs['pk_module'])
        except Module.DoesNotExist:
            raise Http404("The module doesn't exists")

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.save(self.module)
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programmers"] = self.module.project.users.all()
        context["programming_languages"] = ProgrammingLanguage.objects.all()
        context["pk_module"] = self.module.pk

        return context
    

    def get_success_url(self):
        # TODO Redirigir a Detail Program
        return reverse_lazy('programs:list_programs', kwargs={'pk_module': self.module.pk})
