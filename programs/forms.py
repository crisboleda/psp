
# Django
from django import forms

from django.contrib.sessions.middleware import SessionMiddleware

# Models
from programs.models import Program, ProgrammingLanguage, BasePart
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


class CreateBasePartForm(forms.Form):

    base_program = forms.IntegerField()

    base_lines = forms.IntegerField(min_value=1)

    edited_lines = forms.IntegerField()

    deleted_lines = forms.IntegerField()

    added_lines = forms.IntegerField()


    def clean_base_program(self):
        pk_program = self.cleaned_data['base_program']

        try:
            return Program.objects.get(pk=int(pk_program))
        except Program.DoesNotExist:
            raise forms.ValidationError("The program doesn't exists")

    def save(self, program):
        data = self.cleaned_data
        
        BasePart.objects.create(
            program=program,
            program_base=data['base_program'],
            lines_planned_base=data['base_lines'],
            lines_planned_deleted=data['deleted_lines'],
            lines_planned_edited=data['edited_lines'],
            lines_planned_added=data['added_lines']
        )




    