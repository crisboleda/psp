# Django
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.http.response import Http404
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum, F
from django.db.models.functions import Coalesce
from django.contrib import messages

# Models
from programs.models import Program, ProgrammingLanguage, BasePart, ReusedPart, NewPart
from logs.models import Phase
from projects.models import Module
from django.contrib.auth.models import User

# Forms
from programs.forms import CreateProgramForm, UpdateProgramProgrammerForm

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
    paginate_by = 6

    def get_queryset(self):
        return Program.objects.filter(programmer=self.request.user)
    

# Vista que se responde cuando se abre un programa
class DetailProgramView(MemberUserProgramRequiredMixin, DetailView):
    model = Program
    template_name = 'programs/summary/program_opened.html'
    pk_url_kwarg = 'pk_program'
    context_object_name = 'program_opened'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_reused_programs"] = ReusedPart.objects.filter(program__programmer=self.program.programmer).aggregate(reused=Sum('current_lines'))
        context["total_lines_programs"] = Program.objects.filter(programmer=self.program.programmer).aggregate(total=Sum('total_lines'))
        context["total_new_parts_programs"] = NewPart.objects.filter(program__programmer=self.program.programmer).aggregate(total=Sum('current_lines'))

        context["total_base_parts"] = BasePart.objects.filter(program=self.program).aggregate(total_planned_base_lines=Coalesce(Sum('lines_planned_base'), 0), total_planned_deleted_lines=Coalesce(Sum('lines_planned_deleted'), 0), total_planned_edited_lines=Coalesce(Sum('lines_planned_edited'), 0), total_planned_added_lines=Coalesce(Sum('lines_planned_added'), 0), total_current_base_lines=Coalesce(Sum('lines_current_base'), 0), total_current_deleted_lines=Coalesce(Sum('lines_current_deleted'), 0), total_current_edited_lines=Coalesce(Sum('lines_current_edited'), 0), total_current_added_lines=Coalesce(Sum('lines_current_added'), 0))
        context["total_reused_parts"] = ReusedPart.objects.filter(program=self.program).aggregate(planning=Coalesce(Sum('planned_lines'), 0), current=Coalesce(Sum('current_lines'), 0))
        context["total_new_parts"] = NewPart.objects.filter(program=self.program).aggregate(planning=Coalesce(Sum('planning_lines'), 0), current=Coalesce(Sum('current_lines'), 0))

        context["plan_added_lines"] = context["total_new_parts"]["planning"] + context["total_base_parts"]["total_planned_added_lines"]
        context["lines_added_and_modified_plan"] = context["plan_added_lines"] + context["total_base_parts"]["total_planned_edited_lines"]

        context["total_lines_plan"] = context["total_base_parts"]["total_planned_base_lines"] - context["total_base_parts"]["total_planned_deleted_lines"] + context["plan_added_lines"] + context["total_reused_parts"]["planning"]

        # Total lines - (Base actual - Deleted actual + Reused actual)
        context["actual_added_lines"] = self.program.total_lines - (context["total_base_parts"]["total_current_base_lines"] - context["total_base_parts"]["total_current_deleted_lines"] + context["total_reused_parts"]["current"])
        context["lines_added_and_modified_actual"] = context["actual_added_lines"] + context["total_base_parts"]["total_current_edited_lines"]

        return context
    


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




class ConfigurationProgramProgrammerView(MemberUserProgramRequiredMixin, UpdateView):
    template_name = 'programs/settings_program.html'
    queryset = Program.objects.all()
    form_class = UpdateProgramProgrammerForm
    context_object_name = 'detail_program'
    pk_url_kwarg = 'pk_program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program_opened"] = self.program 
        return context

    def get_success_url(self):
        messages.info(self.request, "The program was updated successfully")
        return reverse_lazy('programs:settings_program', kwargs={'pk_program': self.program.pk})