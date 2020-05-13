
# Django
from django import forms

# Models
from logs.models import Phase, TimeLog


class CreateLogProgramForm(forms.Form):

    name_phase = forms.CharField(max_length=20)
    comments = forms.CharField(max_length=100)

    def clean(self):
        try:
            self.phase = Phase.objects.get(name=self.cleaned_data['name_phase'])
        except Phase.DoesNotExist:
            forms.ValidationError("The phase doesn't exists")

    
    def save(self, program):
        data = self.cleaned_data
        TimeLog.objects.create(phase=self.phase, program=program, comments=data['comments'])