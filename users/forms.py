
# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import ExperienceCompany, PositionCompany, Profile


class UserUpdateForm(forms.ModelForm):

    genere = forms.CharField(max_length=12)
    username = forms.CharField(max_length=15, min_length=4, widget=forms.TextInput(
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
                raise forms.ValidationError('El username ya existe actualmente')
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('El email ya existe actualmente')
        return email

    def save(self, user):
        data = self.cleaned_data
        profile = user.get_profile

        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        profile.genere = data['genere']

        user.save()
        profile.save()

        return user


class CreateUserForm(forms.ModelForm):

    confirm_password = forms.CharField(max_length=55)
    username = forms.CharField(min_length=3, max_length=15)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo que intentas registrar ya está en uso")

        return email


    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confirm_password != password:
            raise forms.ValidationError("La contraseña no coincide")


    def save(self):
        data = self.cleaned_data
        data.pop('confirm_password')
        
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)

    


class CreateExperencieCompanyForm(forms.Form):

    name_company = forms.CharField(max_length=70)

    position_company = forms.CharField(max_length=70)

    years_position = forms.IntegerField(min_value=1, max_value=120)

    def clean_position_company(self):
        data = self.cleaned_data["position_company"]
        try:
            return PositionCompany.objects.get(name=data)
        except PositionCompany.DoesNotExist:
            raise forms.ValidationError("The position doesn't exists")
    

    def save(self, user):
        data = self.cleaned_data
        data["user"] = user
        ExperienceCompany.objects.create(**data)