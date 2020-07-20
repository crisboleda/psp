
# Django
from django.test import TestCase


# Forms
from programs.forms import CreateListPip

# Utils
from datetime import datetime


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