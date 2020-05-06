
# Django
from django.urls import reverse, reverse_lazy
from django.http.response import Http404


# Verifica si el usuario está autenticado y que además sea admin
class AdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse(reverse_lazy('users:login'))

        if request.user.get_profile.type_user != 'administrador':
            raise Http404("You aren't an Admin, only Admins can create projects")

        return super().dispatch(request, *args, **kwargs)