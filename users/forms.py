
# Django
from django import forms
from django.utils.translation import gettext as _
from django.conf import settings

# Models
from django.contrib.auth.models import User
from users.models import ExperienceCompany, PositionCompany, Profile

# Utils
from users.utils import GENERES
from services.email import EmailService
import threading
import random


class UserUpdateForm(forms.ModelForm):

    genere = forms.CharField(max_length=12)
    username = forms.CharField(max_length=15, min_length=3)
    email = forms.EmailField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control input-profile',
                'id': 'emailInput',
                'disabled': 'true'
            })
        }

    def clean_genere(self):
        genere = self.cleaned_data["genere"]
        if genere not in GENERES:
            raise forms.ValidationError(_("The genere isn't allowed"))
        return genere


    def clean_username(self):
        username = self.cleaned_data['username']
        if 'username' in self.changed_data:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(_('The username already exists'))
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(_('The email already exists'))
        return email

    def save(self, user):
        data = self.cleaned_data
        profile = user.get_profile

        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        profile.genere = data['genere']

        user.save()
        profile.save()

        return user


class CreateUserForm(forms.ModelForm):

    confirm_password = forms.CharField(max_length=55)
    username = forms.CharField(min_length=3, max_length=15)
    email = forms.EmailField(max_length=55, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("The email you are trying to register is already in use"))

        return email


    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confirm_password != password:
            raise forms.ValidationError(_("Passwords do not match"))


    def save(self):
        data = self.cleaned_data
        data.pop('confirm_password')
        
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)

        data_email = {
            'to_user': user,
            'subject': 'Welcome to PSP',
            'template_name': 'users/registered_user.html',
            'context': {
                'user': user,
                'password_user': data['password']
            }
        }

        if settings.DEBUG:
            EmailService.send_email_local(**data_email)
        else:
            EmailService.send_email_production(**data_email)


class CreateExperencieCompanyForm(forms.Form):

    name_company = forms.CharField(max_length=30)

    position_company = forms.CharField(max_length=70)

    years_position = forms.IntegerField(min_value=1, max_value=120)

    def clean_position_company(self):
        data = self.cleaned_data["position_company"]
        try:
            return PositionCompany.objects.get(name=data)
        except PositionCompany.DoesNotExist:
            raise forms.ValidationError(_("The position doesn't exists"))
    

    def save(self, user):
        data = self.cleaned_data
        data["user"] = user
        ExperienceCompany.objects.create(**data)