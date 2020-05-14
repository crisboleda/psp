
# Django
from django.test import TestCase


class ConvertTimeTestCase(TestCase):

    def setUp(self):
        self.total_time = 3752

        self.hours = 1
        self.minutes = 2
        self.seconds = 32

    def test_calculate_hours(self):
        hours = int(self.total_time / 3600)

        self.assertEquals(hours, self.hours)


    def test_calculate_minutes(self):
        minutes = int((self.total_time % 3600) / 60)

        self.assertEquals(minutes, self.minutes)

    
    def test_calculate_seconds(self):
        seconds = int((self.total_time % 60) % 60)

        self.assertEquals(seconds, self.seconds)
