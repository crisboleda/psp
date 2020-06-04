
# Django
from django.views.generic import TemplateView, DetailView, UpdateView, RedirectView
from django.http.response import JsonResponse, Http404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Django REST Framework
from rest_framework.generics import RetrieveUpdateAPIView

# Serializers
from users.serializers import ProfileExperencieSerializer

# Models
from django.contrib.auth.models import User
from users.models import Profile
from programs.models import ProgrammingLanguage

# Mixins
from users.mixins import AuthenticateOwnerProfileMixin, IsOwnerProfilePermission



def update_experencie_languages(request):
    if request.user.is_authenticated:
        languages = request.GET['languages'].split(',')
        request.user.get_profile.experience_languages.clear()

        for name_language in languages:
            try:
                language = ProgrammingLanguage.objects.get(name=name_language)
                request.user.get_profile.experience_languages.add(language)
            except ProgrammingLanguage.DoesNotExist:
                return Http404('The language not exists')
    
    return JsonResponse(data={"OK": "Yes"})


class UpdateImageProfile(AuthenticateOwnerProfileMixin, UpdateView):
    model = Profile
    fields = ('picture',)

    def get_success_url(self):
        return reverse_lazy('users:profile_user', kwargs={'slug': self.request.user.username})


class DeleteImageProfile(AuthenticateOwnerProfileMixin, RedirectView):

    def get_redirect_url(self, pk):
        profile = self.get_object()
        profile.picture.delete()
        profile.save()
        
        return reverse_lazy('users:profile_user', kwargs={'slug': self.request.user.username})

    def get_object(self):
        pk_profile = self.kwargs['pk']
        try:
            return Profile.objects.get(pk=pk_profile)
        except Profile.DoesNotExist:
            raise Http404("The profile not exists")



class ListUpdateExperencieProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerProfilePermission]
    queryset = Profile.objects.all()
    lookup_url_kwarg = 'pk_profile_user'
    serializer_class = ProfileExperencieSerializer

        