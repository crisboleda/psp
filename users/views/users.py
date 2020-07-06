
# Django
from django.views.generic import ListView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.http.response import Http404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F, Sum, Q, Subquery, OuterRef

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage, Program, BasePart, ReusedPart

# Utils Users
from users.utils import ANALYSIS_TOOLS

# Forms
from users.forms import UserUpdateForm, CreateUserForm

# Mixins
from psp.mixins import AdminRequiredMixin


# View User Login
class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.get_profile.type_user == 'programmer':
            return reverse_lazy('programs:programs_programmer')
        else:
            return reverse_lazy('projects:list_projects')


class RegisterUserView(AdminRequiredMixin, FormView):
    model = User
    template_name = 'users/register_users.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "The user was created successfully")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["programmers"] = User.objects.filter(get_profile__type_user='programmer')
        return context
    
    def get_success_url(self):
        return reverse_lazy('users:register')


# View User data Updata
class UserProfileView(LoginRequiredMixin, FormView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile/profile.html'

    def form_valid(self, form):
        self.user = form.save(self.request.user)

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        profile_user = User.objects.get(username=self.kwargs['slug'])
        
        initial = {
            'username': profile_user.username,
            'email': profile_user.email
        }

        return initial

    def get_success_url(self):
        return reverse_lazy('users:profile_user', kwargs={'slug': self.user.username})


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['slug'])
        
        data['profile_user'] = user
        data['generes'] = ['masculino', 'femenino', 'indefinido']
        data['languages'] = ProgrammingLanguage.objects.all()
        data["experencies_companies"] = user.experencies_companies.all()
        data['profile_languages'] = user.get_profile.experience_languages.all()

        return data






class AnalysisToolsProgrammerView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = User.objects.get(username=kwargs['username'], get_profile__type_user='programmer')
            if request.user != self.user:
                raise Http404("You don't have access to this page")

        except User.DoesNotExist:
            raise Http404("The user doesn't exists")

        return super().dispatch(request, *args, **kwargs)

    template_name = 'programs/analysis_tools/graphics.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["analysis_tools_graphics"] = ANALYSIS_TOOLS
        return context
    