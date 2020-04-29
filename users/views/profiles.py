
# Django
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Models
from django.contrib.auth.models import User


class ProfileUserView(DetailView, LoginRequiredMixin):
    queryset = User.objects.all()
    context_object_name = 'profile_user'
    slug_field = 'username'
    template_name = 'users/profile.html'