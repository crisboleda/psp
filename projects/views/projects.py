
# Django
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Models
from programs.models import ProgrammingLanguage

# Forms
from projects.forms import CreateProjectModelForm

# Mixins
from projects.mixins import AdminRequiredMixin


class ListProjectView(TemplateView, LoginRequiredMixin):
    template_name = 'projects/projects.html'


class CreateProjectView(AdminRequiredMixin, FormView):
    template_name = 'projects/create_project.html'
    form_class = CreateProjectModelForm
    success_url = reverse_lazy('projects:list_projects')

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)

    