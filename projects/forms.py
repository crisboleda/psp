
# Django
from django import forms

# Models
from projects.models import Project


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