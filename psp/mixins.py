
# Django
from django.http.response import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse_lazy

# Models
from programs.models import Program
from django.contrib.auth.models import User


# Verifica si el usuario está autenticado y que además sea admin
class AdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:login'))

        if request.user.get_profile.type_user != 'administrador':
            return HttpResponseForbidden("You aren't an Admin, only Admins can create projects")

        return super().dispatch(request, *args, **kwargs)


class MemberUserProgramRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:login'))

        try:
            self.program = Program.objects.get(pk=kwargs['pk_program'])
        except Program.DoesNotExist:
            raise Http404("The program doesn't exists")

        if request.user.get_profile.type_user == 'programmer' and self.program.programmer != request.user:
            return HttpResponseForbidden("You don't have access to this program")

        return super().dispatch(request, *args, **kwargs)