
# Django
from django.urls import reverse, reverse_lazy
from django.http.response import Http404

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from django.contrib.auth.models import User


# This mixin allows to check if a user is authenticated and owner of profile
class AuthenticateOwnerProfileMixin(object):

    def dispatch(self, request, *args, **kwargs):
        profile_user = self.get_object()
        
        if not request.user.is_authenticated:
            return reverse(reverse_lazy('users:login'))

        if request.user != profile_user.user:
            raise Http404("You aren't owner of the profile")

        return super().dispatch(request, *args, **kwargs)


class IsOwnerProfilePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class UserExistMixin():

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = User.objects.get(username=kwargs["username"])
        except User.DoesNotExist:
            raise Http404("The user doesn't exists")

        return super().dispatch(request, *args, **kwargs)


class AllowAccessUserPageMixin():

    def dispatch(self, request, *args, **kwargs):
        if self.user != request.user:
            raise Http404("You don't access to this page")

        return super().dispatch(request, *args, **kwargs)