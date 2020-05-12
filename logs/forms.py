
# Django
from django import forms

# Models
from logs.models import Phase


class CreateLogProgramForm(forms.Form):

    name_phase = forms.CharField(max_length=20)

    def clean(self):
        try:
            self.phase = Phase.objects.get(name=self.cleaned_data['name_phase'])
        except Phase.DoesNotExist:
            forms.ValidationError("The phase doesn't exists")

    
    def save(self):
        print("Hello world")
        import pdb; pdb.set_trace()