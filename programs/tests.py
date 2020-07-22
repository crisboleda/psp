
# Django
from django.test import TestCase
from django.urls import reverse_lazy

# Models
from django.contrib.auth.models import User
from users.models import Profile
from logs.models import Phase
from programs.models import ProgrammingLanguage, Program
from projects.models import Project, Module

# Forms
from programs.forms import CreateListPip, CreateProgramForm

# Utils
from datetime import datetime, date


class FormCreatePIPTestCase(TestCase):

    def setUp(self):
        self.form1 = CreateListPip(data={
            'name': 'Test PIP',
            'date': datetime(2020, 4, 22, 8, 20, 0),
            'problems': 'Test PIP',
            'proposal': 'Test PIP',
            'comment': 'Test PIP'
        })

        self.form2 = CreateListPip(data={
            'name': 'Test PIP #2'
        })


    # Validate Form is valid
    def test_form_is_valid(self):
        self.assertTrue(self.form1.is_valid())


    # Validate Form isn't valid
    def test_form_is_invalid(self):
        self.assertEquals(len(self.form2.errors), 4)



class FormCreateProgramTestCase(TestCase):

    def setUp(self):

        User.objects.create_user(username='bycristhian', email='by@gmail.com', password='by123')
        ProgrammingLanguage.objects.create(name='Python')

        self.form1 = CreateProgramForm(data={
            'username_programmer': 'bycristhian',
            'name_programming_language': 'Python',
            'name': 'Test name program',
            'description': 'This description must be 50 or greater characteres',
            'start_date': date(2020, 7, 21),
            'planning_date':  date(2020, 7, 31)
        })

        self.form2 = CreateProgramForm(data={
            'username_programmer': 'Nothing',
            'name_programming_language': 'JavaScript',
            'name': 'Test Form 2 Name program',
            'description': 'This description must be 50 or greater characteres',
            'start_date': date(2020, 7, 21),
            'planning_date': date(2020, 7, 20)
        })


    def test_form1_is_valid(self):
        self.assertTrue(self.form1.is_valid())


    def test_form2_user_not_exists(self):
        self.assertFalse(self.form2.is_valid())
        self.assertEqual(self.form2.errors['username_programmer'][0], "The programmer doesn't exists")


    def test_form2_language_not_exists(self):
        self.assertFalse(self.form2.is_valid())
        self.assertEqual(
            self.form2.errors['name_programming_language'][0], 
            "The programming language doesn't exists"
        )

    def test_form2_dates_incorrect(self):
        self.assertFalse(self.form2.is_valid())
        self.assertEqual(
            self.form2.errors['planning_date'][0],
            "The planning date cannot be less than the start date"
        )



class AccessProgramProgrammerTestCase(TestCase):

    def setUp(self):
        self.language = ProgrammingLanguage.objects.create(name='Python')

        self.phase = Phase.objects.create(
            name='Unit Test', 
            abbreviation='UT', 
            description='This phase is Unit Testing',
            order_index=5
        )

        self.admin = User.objects.create_user(
            username='Admin1',
            email='admin@gmail.com',
            password='admin123'
        )
        self.user1 = User.objects.create_user(
            username='User1', 
            email='user@gmail.com', 
            password='user123'
        )
        self.user2 = User.objects.create_user(
            username='User2', 
            email='user2@gmail.com', 
            password='user456'
        )

        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        self.profile3 = Profile.objects.create(user=self.admin, type_user='administrador')

        self.project = Project.objects.create(
            name='Project Test 1', 
            description='This description must be 50 or greater characteres',
            start_date=date(2020, 7, 20),
            planning_date=date(2020, 7, 31),
            admin=self.admin
        )

        self.module = Module.objects.create(
            project=self.project, 
            name='Module Test 1',
            description='This description must be 50 or greater characteres',
            start_date=date(2020, 7, 20),
            planning_date=date(2020, 7, 25)
        )

        self.program1 = Program.objects.create(
            name='Program Test 1',
            description='This description must be 50 or greater characteres',
            programmer=self.user1,
            language=self.language,
            module=self.module,
            start_date=date(2020, 7, 21),
            planning_date=date(2020, 7, 23)
        )

        self.url_program = reverse_lazy('programs:detail_program', kwargs={'pk_program': self.program1.pk})


    def test_user_not_authenticated(self):
        response = self.client.get(self.url_program)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('users:login'))


    def test_user_allowed(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(self.url_program)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='programs/summary/program_opened.html')


    def test_user_not_allowed(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(self.url_program)

        self.assertEqual(response.status_code, 403)