
# Django
from django.urls import reverse, reverse_lazy
from django.http.response import Http404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Models
from projects.models import Project


class MemberProjectRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:login'))
        
        try:
            self.project = Project.objects.get(pk=self.kwargs['pk_project'])
            if request.user not in self.project.users.all() and request.user.get_profile.type_user != 'administrador':
                raise PermissionDenied()

        except Project.DoesNotExist:
            raise Http404("The project doesn't exists")

        return super().dispatch(request, *args, **kwargs)