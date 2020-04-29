
# Django
from django.views.generic import ListView
from django.contrib.auth.views import LoginView

# Models
from django.contrib.auth.models import User


class LoginUserView(LoginView):
    template_name = 'users/login.html'