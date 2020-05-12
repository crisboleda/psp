
# Django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'base/dashboard.html'


class HomeView(TemplateView):
    template_name = 'home.html'


class IndexView(TemplateView):
    template_name = 'index.html'