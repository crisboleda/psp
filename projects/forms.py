
# Django
from django import forms
from django.http.response import Http404

# Models
from projects.models import Project, Module
from django.contrib.auth.models import User

# Estados de un proyecto
from projects.utils import CHOICES_STATUS_PROJECT


class CreateProjectModelForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'planning_date')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control w-100',
                'placeholder': 'Descripción del proyecto',
                'rows': '5',
                'style': 'resize: none'
            })
        }

    
    def save(self, user):
        data = self.cleaned_data
        Project.objects.create(
            name=data['name'],
            description=data['description'],
            planning_date=data['planning_date'],
            admin=user
        )


class UpdateProjectModelForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'description', 'status', 'planning_date')
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


class AddProgrammerProjectForm(forms.Form):

    username_programmer = forms.CharField(max_length=20)

    def clean(self):
        try:
            self.programmer = User.objects.get(username=self.cleaned_data['username_programmer'])
        except User.DoesNotExist:
            raise Http404("The programmer doesn't exists")


    def save(self, project):
        if not self.programmer in project.users.all():
            project.users.add(self.programmer)
        else:
            raise Http404("The programmer already belongs to the project")



class CreateModuleForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('name', 'description', 'planning_date')
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

    def save(self, project):
        data = self.cleaned_data

        Module.objects.create(
            name=data['name'], 
            description=data['description'],
            project=project,
            planning_date=data['planning_date']
        )


class UpdateModuleForm(forms.ModelForm):

    finish_date = forms.DateTimeField(required=False)

    class Meta:
        model = Module
        fields = ('name', 'description', 'planning_date', 'finish_date')
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
