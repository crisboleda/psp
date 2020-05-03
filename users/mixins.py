
from django.urls import reverse, reverse_lazy
from django.http.response import Http404

# This mixin allows to check if a user is authenticated and owner of profile

class AuthenticateOwnerProfileMixin(object):

    def dispatch(self, request, *args, **kwargs):
        profile_user = self.get_object()
        
        if not request.user.is_authenticated:
            return reverse(reverse_lazy('users:login'))

        if request.user != profile_user.user:
            raise Http404("You aren't owner of the profile")

        return super().dispatch(request, *args, **kwargs)