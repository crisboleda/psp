
# Django
from django import forms

from django.contrib.sessions.middleware import SessionMiddleware

# Models
from programs.models import Program, ProgrammingLanguage, BasePart, ReusedPart, NewPart, TypePart, SizeEstimation, Estimation, Report, Pip
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

    
    def clean_lines_current(self):
        if self.cleaned_data['lines_current'] == None:
            return 0
        return self.cleaned_data['lines_current']
    

    def save(self, program):
        data = self.cleaned_data

        ReusedPart.objects.create(
            program=program,
            program_reused_part=data['reused_program'],
            planned_lines=data['lines_planning'],
            current_lines=data['lines_current']
        )


class CreateNewPartForm(forms.Form):

    name_part = forms.CharField(max_length=150)

    type_part = forms.CharField(max_length=30)

    size_estimation = forms.CharField(max_length=2)

    planning_methods = forms.IntegerField(max_value=2000000000, min_value=1)

    current_methods = forms.IntegerField(max_value=2000000000, min_value=0, required=False)
    current_lines = forms.IntegerField(max_value=2000000000, min_value=0, required=False)


    def clean_type_part(self):
        type_part = self.cleaned_data['type_part']

        try:
            return TypePart.objects.get(name=type_part)
        except TypePart.DoesNotExist:
            raise forms.ValidationError("The type part doesn't exists")
    
    
    def clean_current_methods(self):
        if self.cleaned_data['current_methods'] == None:
            return 0
        return self.cleaned_data['current_methods']

    
    def clean_current_lines(self):
        if self.cleaned_data['current_lines'] == None:
            return 0
        return self.cleaned_data['current_lines']

    
    def clean_size_estimation(self):
        size_estimation = self.cleaned_data['size_estimation']

        try:
            return SizeEstimation.objects.get(name=size_estimation)
        except SizeEstimation.DoesNotExist:
            raise forms.ValidationError("The size estimation doesn't exists")


    def clean(self):
        data = self.cleaned_data

        try:
            self.estimation = Estimation.objects.get(type_part=data['type_part'], size_estimation=data['size_estimation'])
            self.planning_lines = data['planning_methods'] * self.estimation.lines_of_code
        except Estimation.DoesNotExist:
            raise forms.ValidationError("The estimation doesn't exists")

        return data


    def save(self, program):
        data = self.cleaned_data

        NewPart.objects.create(
            name=data['name_part'],
            program=program,
            estimation=self.estimation,
            planning_methods=data['planning_methods'],
            planning_lines=self.planning_lines,
            current_methods=data['current_methods'],
            current_lines=data['current_lines']
        )


    
class CreateReportModelForm(forms.ModelForm):

    current_results = forms.CharField(max_length=350, required=False)

    class Meta:
        model = Report
        fields = ('date', 'name', 'objetive', 'description', 'conditions', 'expect_results', 'current_results')


    def save(self, program):
        data = self.cleaned_data
        data['program'] = program

        Report.objects.create(**data)


class CreateListPip(forms.ModelForm):

    class Meta:
        model = Pip
        fields = ('name','date','problems','proposal','comment')

    def save(self, program):
        data = self.cleaned_data
        data['program'] = program

        Pip.objects.create(**data)