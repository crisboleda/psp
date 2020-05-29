
# Django
from django import forms

from django.contrib.sessions.middleware import SessionMiddleware

# Models
from programs.models import Program, ProgrammingLanguage, BasePart, ReusedPart, NewPart
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

    base_lines = forms.IntegerField(min_value=1, max_value=2000000000)

    edited_lines = forms.IntegerField(min_value=0, max_value=2000000000, required=False)

    deleted_lines = forms.IntegerField(min_value=0, max_value=2000000000, required=False)

    added_lines = forms.IntegerField(min_value=0, max_value=2000000000, required=False)


    def clean_base_program(self):
        pk_program = self.cleaned_data['base_program']

        try:
            return Program.objects.get(pk=int(pk_program))
        except Program.DoesNotExist:
            raise forms.ValidationError("The program doesn't exists")

    def clean_edited_lines(self) -> int:
        return self.is_null(self.cleaned_data['edited_lines'])

    def clean_deleted_lines(self) -> int:
        return self.is_null(self.cleaned_data['deleted_lines'])

    def clean_added_lines(self) -> int:
        return self.is_null(self.cleaned_data['added_lines'])

    def is_null(self, value) -> int:
        if value == None:
            return 0
        return value


    def clean(self):
        data = self.cleaned_data
        if data['deleted_lines'] > data['base_lines'] or data['edited_lines'] > (data['base_lines'] - data['deleted_lines']):
            raise forms.ValidationError("There is no base lines")

        return data
    

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



class CreateReusedPartForm(forms.Form):

    reused_program = forms.IntegerField()

    lines_planning = forms.IntegerField(min_value=1, max_value=2000000000)

    lines_current = forms.IntegerField(required=False, min_value=0, max_value=2000000000)

    
    def clean_reused_program(self):
        pk_program = self.cleaned_data['reused_program']

        try:
            return Program.objects.get(pk=pk_program)
        except Program.DoesNotExist:
            raise forms.ValidationError("The program doesn't exists")
    

    def save(self, program):
        data = self.cleaned_data

        ReusedPart.objects.create(
            program=program,
            program_reused_part=data['reused_program'],
            planned_lines=data['lines_planning'],
            current_lines=data['lines_current']
        )


    