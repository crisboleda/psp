# Django
from django.views.generic import ListView, FormView, DetailView
from django.http.response import Http404
from django.urls import reverse_lazy

# Models
from programs.models import Program, ProgrammingLanguage
from projects.models import Module

# Forms
from programs.forms import CreateProgramForm

# Mixins
from psp.mixins import AdminRequiredMixin, MemberUserProgramRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class AdminListProgramView(AdminRequiredMixin, ListView):
    template_name = 'programs/programs.html'
    context_object_name = 'programs'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.module = Module.objects.get(pk=kwargs['pk_module'])
        except Module.DoesNotExist:
            raise Http404("The module doesn't exists")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Program.objects.filter(module=self.module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["module"] = self.module 
        return context
    


# Vista que muestra todos los programas que tiene un programador
class ProgrammerListProgramView(LoginRequiredMixin, ListView):
    template_name = 'programs/programs_programmer.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.filter(programmer=self.request.user)


# Vista que se responde cuando se abre un programa
class DetailProgramView(MemberUserProgramRequiredMixin, DetailView):
    model = Program
    template_name = 'programs/program_opened.html'
    pk_url_kwarg = 'pk_program'
    context_object_name = 'program_opened'


# Vista para crear un programa (Solo pueden acceder administradores)
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
