
# Django
from django import forms

from django.contrib.sessions.models import Session

# Models
from programs.models import Program, ProgrammingLanguage
from django.contrib.auth.models import User


class CreateProgramForm(forms.ModelForm):

    username_programmer = forms.CharField(max_length=15, min_length=4)
    name_programming_language = forms.CharField(max_length=100)

    class Meta:
        model = Program
        fields = ('name', 'description', 'planning_date')


    def clean_username_programmer(self):
        username_programmer = self.cleaned_data['username_programmer']
        try:
            self.programmer = User.objects.get(username=username_programmer)
        except User.DoesNotExist:
            raise forms.ValidationError("The programmer doesn't exists")

        return username_programmer

    
    def clean_name_programming_language(self):
        name_programming_language = self.cleaned_data['name_programming_language']
        try:
            self.programming_language = ProgrammingLanguage.objects.get(name=name_programming_language)
        except ProgrammingLanguage.DoesNotExist:
            raise forms.ValidationError("The programming language doesn't exists")

        return name_programming_language


    def save(self, module):
        data = self.cleaned_data

        Program.objects.create(
            name=data['name'],
            description=data['description'],
            programmer=self.programmer,
            language=self.programming_language,
            module=module,
            planning_date=data['planning_date']
        )

    