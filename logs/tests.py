
# Django
from django.test import TestCase

# Models
from logs.models import Phase

# Forms
from logs.forms import CreateLogProgramForm


# Dividir segundos a horas, minutos y segundos
class ConvertTimeTestCase(TestCase):

    def setUp(self):
        self.total_time = 3752

        self.hours = 1
        self.minutes = 2
        self.seconds = 32

    # Calculare hours
    def test_calculate_hours(self):
        hours = int(self.total_time / 3600)

        self.assertEquals(hours, self.hours)


    # Calculate minutes
    def test_calculate_minutes(self):
        minutes = int((self.total_time % 3600) / 60)

        self.assertEquals(minutes, self.minutes)

    
    # Calculate seconds
    def test_calculate_seconds(self):
        seconds = int((self.total_time % 60) % 60)

        self.assertEquals(seconds, self.seconds)



# Form for Create Time Log 
class FormCreateTimeLogTestCase(TestCase):

    def setUp(self):
        self.phase = Phase.objects.create(
            name='Codification', 
            abbreviation='CD', 
            description='Phase of code',
            order_index=4
        )

        self.form1 = CreateLogProgramForm(data={
            'name_phase': 'Codification',
            'comments': 'This phase is codification :D'
        })

        self.form2 = CreateLogProgramForm(data={
            'name_phase': 'Test',
        })


    def test_form_is_valid(self):
        self.assertTrue(self.form1.is_valid())


    def test_phase_not_exists(self):
        self.assertEqual(self.form2.errors['comments'][0], 'This field is required.')
        self.assertEqual(self.form2.errors['__all__'][0], "The phase doesn't exists")
        self.assertEqual(len(self.form2.errors), 2)
