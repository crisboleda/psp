
# Django
from django.views.generic import ListView

# Models
from django.contrib.auth.models import User


class LoginView(ListView):
    queryset = User.objects.all()
    template_name = 'users/login.html'