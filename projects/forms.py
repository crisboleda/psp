
# Django
from django import forms
from django.http.response import Http404
from django.utils.translation import gettext as _

# Models
from projects.models import Project, Module
from django.contrib.auth.models import User

# Estados de un proyecto
from projects.utils import CHOICES_STATUS_PROJECT


class CreateProjectModelForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'start_date', 'planning_date')
    
    def clean_planning_date(self):
        planning_date = self.cleaned_data["planning_date"]

        if planning_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError(_("The planning date cannot be less than the start date")) 
        return planning_date
        

    def save(self, user):
        data = self.cleaned_data
        Project.objects.create(
            name=data['name'],
            description=data['description'],
            start_date=data["start_date"],
            planning_date=data['planning_date'],
            admin=user
        )


class UpdateProjectModelForm(forms.ModelForm):

    finish_date = forms.DateField(required=False)

    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'start_date', 'planning_date', 'finish_date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'style': 'resize: none;',
                'rows': '5'
            }),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                },
                choices=CHOICES_STATUS_PROJECT
            ),
        }

    def clean_planning_date(self):
        planning_date = self.cleaned_data["planning_date"]

        if planning_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError(_("The planning date cannot be less than the start date"))
        return planning_date


    def clean_finish_date(self):
        finish_date = self.cleaned_data["finish_date"]

        if finish_date != None and (finish_date < self.cleaned_data["start_date"] or finish_date < self.cleaned_data["planning_date"]):
            raise forms.ValidationError(_("The finish date cannot be less than the start date and planning date"))
        return finish_date


class AddProgrammerProjectForm(forms.Form):

    username_programmer = forms.CharField(max_length=50, required=True)

    def clean_username_programmer(self):
        username = self.cleaned_data['username_programmer']
        try:
            self.programmer = User.objects.get(username=self.cleaned_data['username_programmer'])
        except User.DoesNotExist:
            raise forms.ValidationError(_("The programmer doesn't exists"))

        return username


    def save(self, project):
        if not self.programmer in project.users.all():
            project.users.add(self.programmer)



class CreateModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('name', 'description', 'start_date', 'planning_date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': '5',
                'style': 'resize: none'
            })
        }

    def clean_planning_date(self):
        planning_date = self.cleaned_data["planning_date"]

        if planning_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError(_("The planning date cannot be less than the start date"))
        return planning_date

    def save(self, project):
        data = self.cleaned_data

        Module.objects.create(
            name=data['name'], 
            description=data['description'],
            project=project,
            start_date=data["start_date"],
            planning_date=data['planning_date']
        )


class UpdateModuleForm(forms.ModelForm):

    finish_date = forms.DateField(required=False)

    class Meta:
        model = Module
        fields = ('name', 'description', 'start_date', 'planning_date', 'finish_date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'rows': '5',
                'style': 'resize: none'
            })
        }

    def clean_planning_date(self):
        planning_date = self.cleaned_data["planning_date"]

        if planning_date <= self.cleaned_data["start_date"]:
            raise forms.ValidationError(_("The planning date cannot be less than the start date"))
        return planning_date


    def clean_finish_date(self):
        finish_date = self.cleaned_data["finish_date"]

        if finish_date != None and (finish_date < self.cleaned_data["planning_date"] or finish_date < self.cleaned_data["start_date"]):
            raise forms.ValidationError(_("The finish date cannot be less than the start date and planned date"))
        return finish_date