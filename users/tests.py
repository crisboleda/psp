
# Django
from django.test import TestCase
from django.contrib.auth import authenticate

# Models
from django.contrib.auth.models import User


class UserAuthenticateTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='cristhian', email='cristhian@gmail.com', password='123')
        self.user2 = User.objects.create_user(username='laura', email='laura@gmail.com', password='lol')

    def test_authenticate_user_username(self):
        username = 'cristhian'
        password = '123'

        user = authenticate(username=username, password=password)

        self.assertEquals(user, self.user1)


    def test_authenticate_user_email(self):
        email = 'laura@gmail.com'
        password = 'lol'

        user = authenticate(username=email, password=password)

        self.assertEquals(user, self.user2)