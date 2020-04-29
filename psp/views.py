
# Django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(TemplateView, LoginRequiredMixin):
    template_name = 'base/dashboard.html'