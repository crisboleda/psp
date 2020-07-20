
# Django
from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.urls import reverse_lazy

# Models
from django.contrib.auth.models import User
from users.models import Profile
from users.models import PositionCompany, ExperienceCompany, Profile
from programs.models import ProgrammingLanguage


class UserAuthenticateTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='cristhian', email='cristhian@gmail.com', password='123')
        self.user2 = User.objects.create_user(username='laura', email='laura@gmail.com', password='lol')

        self.username_user1 = 'cristhian'
        self.password_user1 = '123'

        self.email_user2 = 'laura@gmail.com'
        self.password_user2 = 'lol'

    # Test authentication with username and password
    def test_authenticate_user_username(self):

        user = authenticate(username=self.username_user1, password=self.password_user1)
        self.assertEquals(user, self.user1)


    # Test authentication with email and password
    def test_authenticate_user_email(self):

        user = authenticate(username=self.email_user2, password=self.password_user2)
        self.assertEquals(user, self.user2)



# Funcionalidad de agregar y remover lenguajes a experencia
class ExperencieLanguageProfileTest(TestCase):

    def setUp(self):
        self.langauge1 = ProgrammingLanguage.objects.create(name='Python')
        self.langauge2 = ProgrammingLanguage.objects.create(name='JavaScript')

        self.user = User.objects.create(username='user1', email='user1@gmail.com', password='user123')
        self.profile = Profile.objects.create(user=self.user)


    def add_languages(self):
        self.profile.experience_languages.add(self.langauge1)
        self.profile.experience_languages.add(self.langauge2)


    # Add language into profile experencie
    def test_add_language(self):
        self.add_languages()
        self.assertEquals(self.profile.experience_languages.count(), 2)

    
    # Remove language from profile experencie
    def test_remove_language(self):
        self.add_languages()

        self.profile.experience_languages.remove(self.langauge2)
        self.assertEquals(self.profile.experience_languages.count(), 1)
        


# Validate Access and Response the endpoint of calendar
class AdminCalendarViewTestCase(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username='admin', 
            email='email@gmail.com', 
            password='admin123'
        )
        self.profile_administrador = Profile.objects.create(user=self.admin, type_user='administrador')

        self.programmer = User.objects.create_user(
            username='programmer', 
            email='pro@gmail.com', 
            password='pro123'
        )
        self.profile_programmer = Profile.objects.create(user=self.programmer)

        self.url_calendar = reverse_lazy('calendar')

    
    # Validate that admin can get template of calendar
    def test_calendar_GET(self):
        self.client.force_login(user=self.admin)
        response = self.client.get(self.url_calendar)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='users/calendar.html')


    # Validate that user not authenticated can't access the endpoint
    def test_user_not_authenticated(self):
        response = self.client.get(self.url_calendar)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse_lazy('users:login'))


    # Validate that a programmer can't access the endpoint
    def test_user_is_programmer(self):
        self.client.force_login(user=self.programmer)
        response = self.client.get(self.url_calendar)

        self.assertEquals(response.status_code, 403)
