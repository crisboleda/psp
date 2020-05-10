
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
from projects.mixins import MemberProjectRequiredMixin
from psp.mixins import AdminRequiredMixin


class ListProjectView(ListView, LoginRequiredMixin):
    context_object_name = 'projects'
    template_name = 'projects/projects.html'

    def get_queryset(self):
        type_user = self.request.user.get_profile.type_user

        if type_user == 'administrador':
            return Project.objects.all()

        elif type_user == 'programmer':
            return Project.objects.filter(users__id__exact=self.request.user.pk)
            


class CreateProjectView(AdminRequiredMixin, FormView):
    template_name = 'projects/create_project.html'
    form_class = CreateProjectModelForm
    success_url = reverse_lazy('projects:list_projects')

    def form_valid(self, form):
        form.save(self.request.user)
        return super().form_valid(form)


class DetailProjectView(MemberProjectRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/detail_project.html'
    context_object_name = 'project'
    pk_url_kwarg = 'pk_project'


class UpdateProjectView(AdminRequiredMixin, UpdateView):
    model = Project
    pk_url_kwarg = 'pk_project'
    form_class = UpdateProjectModelForm
    context_object_name = 'project'
    template_name = 'projects/edit_project.html'
    success_url = reverse_lazy('projects:list_projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context["programmers"] = User.objects.exclude(id__in=project.users.all()).filter(get_profile__type_user='programmer').only('username')
        return context


class AddProgrammerProjectView(AdminRequiredMixin, FormView):
    form_class = AddProgrammerProjectForm

    def form_valid(self, form):
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            form.save(self.project)
        except Project.DoesNotExist:
            raise Http404("The project doesn't exists")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projects:edit_project', kwargs={'pk': self.project.pk})


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

