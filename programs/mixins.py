
# Django
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse_lazy

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsOwnerProgram(BasePermission):

    def has_object_permission(self, request, view, obj):

        if obj.program.programmer != request.user:
            return False
        return True


class OwnerReportPIPMixin():

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:login'))

        if self.get_object().program.programmer != request.user:
            return HttpResponseForbidden("You don't access to this")

        return super().dispatch(request, *args, **kwargs)