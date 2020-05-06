
# Django
from django.views.generic import FormView, ListView, DetailView, UpdateView, FormView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http.response import Http404

# Models
from programs.models import ProgrammingLanguage
from projects.models import Project
from django.contrib.auth.models import User

# Forms
from projects.forms import CreateProjectModelForm, UpdateProjectModelForm, AddProgrammerProjectForm

# Mixins
from projects.mixins import AdminRequiredMixin


class ListProjectView(ListView, LoginRequiredMixin):
    queryset = Project.objects.all()
    context_object_name = 'projects'
    template_name = 'projects/projects.html'


class CreateProjectView(AdminRequiredMixin, FormView):
    template_name = 'projects/create_project.html'
    form_class = CreateProjectModelForm
    success_url = reverse_lazy('projects:list_projects')

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)


class DetailProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/detail_project.html'
    context_object_name = 'project'


class UpdateProjectView(AdminRequiredMixin, UpdateView):
    model = Project
    form_class = UpdateProjectModelForm
    context_object_name = 'project'
    template_name = 'projects/edit_project.html'
    success_url = reverse_lazy('projects:list_projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context["programmers"] = User.objects.exclude(id__in=project.users.all()).filter(get_profile__type_user='programmer').only('username')
        return context


class UpdateProgrammerProjectView(AdminRequiredMixin, FormView):

    def form_valid(self, form):
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            form.save(self.project)
        except Project.DoesNotExist:
            raise Http404("The project doesn't exists")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:edit_project', kwargs={'pk': self.project.pk})


class AddProgrammerProjectView(UpdateProgrammerProjectView):
    form_class = AddProgrammerProjectForm


class RemoveProgrammerProjectView(AdminRequiredMixin, RedirectView):

    def dispatch(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            self.programmer = User.objects.get(username=self.kwargs['username_programmer'])

            if self.programmer in self.project.users.all():
                self.project.users.remove(self.programmer)
            else:
                raise Http404("The programmer isn't into project")

        except Project.DoesNotExist:
            raise Http404("The project doen't exists")

        except User.DoesNotExist:
            raise Http404("The user doesn't exists")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, pk_project, username_programmer):
        return reverse_lazy('projects:edit_project', kwargs={'pk': pk_project })

