
# Django
from django.db import models

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(
        upload_to='users/profile/', 
        help_text="User profile picture", 
        null=True, 
        blank=True
    )

    custom_choices_type_user = (('programmer', 'Programmer'), ('director', 'Director'))
    type_user = models.CharField(
        max_length=11, 
        choices=custom_choices_type_user, 
        help_text='User rank', 
        default='programmer'
    )

    experience_languages = models.ManyToManyField(ProgrammingLanguage, related_name='experience_languages')

    years_development = models.IntegerField(default=0, help_text='Years of development experience')
    years_configuration = models.IntegerField(default=0, help_text='Years of configuration experience')
    years_integration = models.IntegerField(default=0, help_text='Years of integration experience')
    years_requirements = models.IntegerField(default=0, help_text='Years of requirements experience')
    years_design = models.IntegerField(default=0, help_text='Years of design experience')
    years_tests = models.IntegerField(default=0, help_text='Years of testing experience')
    years_support = models.IntegerField(default=0, help_text='Years of support experience')

    created_at = models.DateTimeField(auto_now_add=True, help_text='User profile creation date')
    updated_at = models.DateTimeField(auto_now=True, help_text='User profile update date')


    def __str__(self):
        return "{} is {}".format(self.user, self.type_user)
    

