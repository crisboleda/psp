
# Django
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from django.contrib.auth.models import User
from programs.models import ProgrammingLanguage


def remove_image_old(instance, filename):
    instance_old = Profile.objects.get(pk=instance.pk)
    instance_old.picture.delete()

    return 'users/profile/{}'.format(filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='get_profile')

    custom_choices_generes = (('masculino', 'Masculino'), ('femenino', 'Femenino'), ('indefinido', 'Indefinido'))

    genere = models.CharField(
        max_length=20,
        choices=custom_choices_generes,
        help_text='Genere of user',
        default='indefinido'
    )

    picture = models.ImageField(
        upload_to=remove_image_old, 
        help_text="User profile picture", 
        null=True, 
        blank=True
    )

    custom_choices_type_user = (('programmer', 'Programmer'), ('administrador', 'Administrador'))
    type_user = models.CharField(
        max_length=15, 
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
    

