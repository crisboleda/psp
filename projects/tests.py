
# Django
from django.test import TestCase

# Models
from django.contrib.auth.models import User
from projects.models import Project

# Utils
from datetime import date


# TestCase Add or Remove programmer to project
class ProgrammerProjectTestCase(TestCase):

    def setUp(self):

        self.admin = User.objects.create(username='admin', email='admin@gmail.com', password='admin123')

        self.project = Project.objects.create(
            name='project1', 
            description='project1', 
            admin=self.admin,
            start_date=date(2020, 4, 5),
            planning_date=date(2020, 4, 22)
        )

        self.user1 = User.objects.create_user(
            username='Juanes', 
            email='juan@gmail.com', 
            password='juan123'
        )

        self.user2 = User.objects.create_user(
            username='Maria', 
            email='maria@gmail.com', 
            password='maria123'
        )


    def add_programmers(self):
        self.project.users.add(self.user1)
        self.project.users.add(self.user2)

    # Add programmer into project
    def test_add_programmer(self):
        self.add_programmers()

        self.assertEquals(self.project.users.count(), 2)
    
    # Remove programmer from project
    def test_remove_programmer(self):
        self.add_programmers()

        self.project.users.remove(self.user1)
        self.assertEquals(self.project.users.count(), 1)
        



# Este test verifica que las fechas de los proyectos tengan correlación
class DateProjectTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create(username='admin', email='admin@gmail.com', password='admin123')

        self.start_date = date(2020, 4, 5)
        self.planning_date = date(2020, 4, 22)

        self.project = Project.objects.create(
            name='project1', 
            description='project1', 
            admin=self.admin,
            start_date=self.start_date,
            planning_date=self.planning_date
        )

    # The start date must be less than the planning date
    def test_start_date(self):
        self.assertLess(self.project.start_date, self.project.planning_date)


    # The finish date must be greater than the planning date and start date
    def test_update_finish_date(self):
        self.project.finish_date = date(2020, 4, 30)
        self.project.save()

        self.assertLessEqual(self.project.planning_date, self.project.finish_date)
        self.assertLess(self.project.start_date, self.project.finish_date)
        

