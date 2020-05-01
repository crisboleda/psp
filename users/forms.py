
# Django
from django import forms

# Models
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):

    genere = forms.CharField(max_length=12)
    username = forms.CharField(max_length=10, min_length=4, widget=forms.TextInput(
        attrs= {
            'class': 'form-control input-profile',
            'id': 'usernameInput',
            'disabled': 'true'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control input-profile',
                'id': 'emailInput',
                'disabled': 'true'
            })
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if 'username' in self.changed_data:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('The username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('The email already exists')
        return email

    def save(self, user):
        data = self.cleaned_data

        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        user.save()

        return user
        

    
