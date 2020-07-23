
# Django
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.utils.translation import gettext as _

# Django REST Framework
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status

# Models
from users.models import ExperienceCompany, PositionCompany

# Mixins and Permissions
from users.mixins import IsOwnerProfilePermission

# Forms
from users.forms import CreateExperencieCompanyForm

# Serializers
from users.serializers import ExperencieCompanySerializer, ExperencieCompanyModelSerializer



class CreateExperencieCompanyView(LoginRequiredMixin, FormView):
    queryset = ExperienceCompany.objects.all()
    form_class = CreateExperencieCompanyForm
    template_name = 'users/profile/edit_experencie_companies.html'
    success_url = reverse_lazy('users:create_experencie_user')

    def form_valid(self, form):
        form.save(self.request.user)
        messages.success(self.request, _("The experencie was created successfully"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experencie_companies"] = ExperienceCompany.objects.filter(user=self.request.user) 
        context["positions"] = PositionCompany.objects.all()
        return context

    
class ExperencieCompanyAPIView(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    queryset = ExperienceCompany.objects.all()
    serializer_class = ExperencieCompanyModelSerializer
    permission_classes = [IsOwnerProfilePermission]
    lookup_url_kwarg = 'pk_exp_company'

    def patch(self, request, *args, **kwargs):
        serializer = ExperencieCompanySerializer(data=request.data)
        if serializer.is_valid():
            messages.info(request, _("The experencie company was updated successfully"))
            experencie = serializer.save(self.get_object())
            return Response(data=self.serializer_class(instance=experencie).data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)