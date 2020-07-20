
# Django
from django import forms

# Models
from logs.models import Phase, TimeLog, DefectType, DefectLog


class CreateLogProgramForm(forms.Form):

    name_phase = forms.CharField(max_length=20)
    comments = forms.CharField(max_length=100)

    def clean(self):
        try:
            self.phase = Phase.objects.get(name=self.cleaned_data['name_phase'])
        except Phase.DoesNotExist:
            raise forms.ValidationError("The phase doesn't exists")


    def save(self, program):
        data = self.cleaned_data
        TimeLog.objects.create(phase=self.phase, program=program, comments=data['comments'])



class CreateDefectLogForm(forms.Form):

    date = forms.DateTimeField()

    defect_type = forms.CharField(max_length=4)

    phase_injected = forms.CharField(max_length=10)

    phase_removed = forms.CharField(max_length=10)

    cousing_defect = forms.CharField(max_length=200, required=False)

    description = forms.CharField(max_length=500)

    solution = forms.CharField(max_length=500)

    time_reparation = forms.IntegerField(min_value=1)


    def clean_defect_type(self):
        try:
            return DefectType.objects.get(number=int(self.cleaned_data['defect_type']))
        except DefectType.DoesNotExist:
            raise forms.ValidationError("The defect type doesn't exists")

    
    def clean_phase_injected(self):
        try:
            return Phase.objects.get(abbreviation=self.cleaned_data['phase_injected'])
        except Phase.DoesNotExist:
            raise forms.ValidationError("The phase doesn't exists")

        return phase


    def clean_phase_removed(self):
        try:
            return Phase.objects.get(abbreviation=self.cleaned_data['phase_removed'])
        except Phase.DoesNotExist:
            raise forms.ValidationError("The phase doesn't exists")


    def clean_cousing_defect(self):
        try:
            if self.cleaned_data['cousing_defect']:   
                return DefectLog.objects.get(pk=int(self.cleaned_data['cousing_defect']))
            return None
        except DefectLog.DoesNotExist:
            raise forms.ValidationError("The defect log doesn't exists")

    
    def save(self, program):
        data = self.cleaned_data

        DefectLog.objects.create(
            program=program,
            defect=data['defect_type'],
            date=data['date'],
            time_reparation=data['time_reparation'],
            phase_injected=data['phase_injected'],
            phase_removed=data['phase_removed'],
            description=data['description'],
            solution=data['solution'],
            cousing_defect=data['cousing_defect']
        )
