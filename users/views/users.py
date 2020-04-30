
# Django
from django.views.generic import ListView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage

# Forms
from users.forms import UserUpdateForm


# View User Login
class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'


# View User data Updata
class UserProfileView(FormView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile/profile.html'

    def form_valid(self, form):
        form.save(self.request.user)

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
        user = User.objects.get(username=self.kwargs['slug'])
        return reverse_lazy('users:profile_user', kwargs={'slug': self.request.user.username})


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['profile_user'] = User.objects.get(username=self.kwargs['slug'])
        data['languages'] = ProgrammingLanguage.objects.all()

        return data