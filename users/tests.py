
# Django
from django.test import TestCase
from django.contrib.auth import authenticate

# Models
from django.contrib.auth.models import User
from users.models import PositionCompany, ExperienceCompany


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