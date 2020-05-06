
# Django
from django.test import TestCase

# Models
from django.contrib.auth.models import User
from projects.models import Project


# TestCase Add or Remove programmer to project
class ProgrammerProjectTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='Juanes', email='juan@gmail.com', password='juan123')
        self.user2 = User.objects.create_user(username='Maria', email='maria@gmail.com', password='maria123')

