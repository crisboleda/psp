# Django
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.http.response import Http404
from django.urls import reverse_lazy
from django.db.models import Count, Q, Sum, F, OuterRef, Subquery
from django.db.models.functions import Coalesce, Ceil
from django.contrib import messages

# Models
from programs.models import Program, ProgrammingLanguage, BasePart, ReusedPart, NewPart
from logs.models import Phase, TimeLog
from projects.models import Module
from django.contrib.auth.models import User

# Forms
from programs.forms import CreateProgramForm, UpdateProgramProgrammerForm, UpdateProgramAdminForm

# Mixins
from psp.mixins import AdminRequiredMixin, MemberUserProgramRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Helpers
from psp.helpers import FormViewDefaultValue

# Utils
from datetime import datetime


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

        context["total_defects_removed"] = Phase.objects.annotate(
            total=Coalesce(Count('name', filter=Q(phase_defect_removed__program=self.program)), 0)
        ).values('name', 'total').filter(name='Unit Test').order_by('created_at')[0]


        base = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_base'))
        edited = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_edited'))
        deleted = BasePart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('lines_current_deleted'))
        reused = ReusedPart.objects.values('program__pk').filter(program=OuterRef("pk")).annotate(total=Sum('current_lines'))

        context["total_lines_added_and_modified"] = Program.objects.values('programmer__pk').filter(programmer=self.program.programmer).annotate(total=Coalesce(Sum(Coalesce((F('total_lines') - (Subquery(base.values('total')) - Subquery(deleted.values('total')) + Subquery(reused.values('total')) )) + Subquery(edited.values('total')), 0)), 0)).values('total')[0]

        # Percentage Reused lines
        context["percentage_reused_actual"] = round(100 * (self.validate_zero_division(context["total_reused_parts"]["current"], self.program.total_lines)), 2)
        context["percentage_reused_to_date"] = round(100 * (self.validate_zero_division(context["total_reused_programs"]["reused"], context["total_lines_programs"]["total"])), 2)
        context["percentage_reused_planned"] = round(100 * (self.validate_zero_division(context["total_reused_parts"]["planning"], context["total_lines_plan"])), 2)

        # Percentage new Lines
        context["percentage_new_lines_plan"] = round(100 * (self.validate_zero_division(context["total_new_parts"]["planning"], context["lines_added_and_modified_plan"])), 2)
        context["percentage_new_lines_actual"] = round(100 * (self.validate_zero_division(context["total_new_parts"]["current"], context["lines_added_and_modified_actual"])), 2)
        context["percentage_new_lines_to_date"] = round(100 * (self.validate_zero_division(context["total_new_parts_programs"]["total"], context["total_lines_added_and_modified"]["total"])), 2)

        context["summary"] = {
            "test_defects": round(1000 * (self.validate_zero_division(context["total_defects_removed"]["total"], context["lines_added_and_modified_actual"])), 2)
        }

        return context

    def validate_zero_division(self, value1, value2):
        try:
            return value1 / value2
        except ZeroDivisionError:
            return 0
    

# Vista para crear un programa (Solo pueden acceder administradores)
class CreateProgramView(AdminRequiredMixin, FormViewDefaultValue):
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
        messages.success(self.request, "The program was created successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programmers"] = self.module.project.users.all()
        context["programming_languages"] = ProgrammingLanguage.objects.all()
        context["pk_module"] = self.module.pk

        return context

    def set_values_init_form(self, form):
        form["start_date"].value = datetime.now()

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



class UpdateProgramAdminView(AdminRequiredMixin, UpdateView):
    template_name = 'programs/edit_program.html'
    queryset = Program.objects.all()
    form_class = UpdateProgramAdminForm
    context_object_name = 'program'
    pk_url_kwarg = 'pk_program'

    def get_success_url(self):
        messages.info(self.request, "The program was updated successfully")
        return reverse_lazy('programs:list_programs', kwargs={'pk_module': self.get_object().module.pk})

