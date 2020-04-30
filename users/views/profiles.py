
# Django
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage


class ProfileUserView(DetailView, LoginRequiredMixin):
    queryset = User.objects.all()
    context_object_name = 'profile_user'
    slug_field = 'username'
    template_name = 'users/profile/profile.html'


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['languages'] = ProgrammingLanguage.objects.all()

        return data


        