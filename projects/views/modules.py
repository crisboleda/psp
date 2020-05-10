
# Django
from django.views.generic import ListView, FormView, UpdateView
from django.http.response import Http404
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

# Models
from projects.models import Module, Project

# Forms
from projects.forms import CreateModuleForm, UpdateModuleForm

# Mixins
from projects.mixins import MemberProjectRequiredMixin
from psp.mixins import AdminRequiredMixin


class ListModuleView(MemberProjectRequiredMixin, ListView):
    template_name = 'modules/modules.html'
    context_object_name = 'modules'

    def get_queryset(self):
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            return Module.objects.filter(project=self.project)
        except Project.DoesNotExist:
            raise Http404("The project doen't exists")

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk_project"] = self.kwargs['pk_project']
        return context
        

class CreateModuleView(AdminRequiredMixin, FormView):
    template_name = 'modules/create_module.html'
    form_class = CreateModuleForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            return super().dispatch(request, *args, **kwargs)
        except Project.DoesNotExist:
            raise Http404("The project doesn't exists")


    def form_valid(self, form):
        form.save(self.project)
        return super().form_valid(form)  


    def get_success_url(self):
        return reverse_lazy('projects:list_modules', kwargs={'pk_project': self.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk_project"] = self.project.pk
        return context
    
        
class UpdateModuleView(UpdateView):
    model = Module
    template_name = 'modules/edit_module.html'
    context_object_name = 'module'
    pk_url_kwarg = 'pk_module'
    form_class = UpdateModuleForm

    def get_success_url(self):
        pk_project = self.kwargs['pk_project']
        pk_module = self.kwargs['pk_module']

        return reverse_lazy('projects:update_module', kwargs={'pk_project': pk_project, 'pk_module': pk_module})