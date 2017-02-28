from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from api.tools import dates

class DatesTestCase(TestCase):

    def test_date2fraction(self):
        """
            Test the output of date2fraction
        """

        expected = {
            '20150101120000' : 0.5,
            '20150102120000' : 1.5,
            '20151231000000' : 364,
        }

        for inline_time in expected:
            time = dates.format_inline_time(inline_time)
            fraction = dates.date2fraction(time)

            self.assertEquals(fraction, expected[inline_time])

    def test_fraction2date(self):
        """
            Test the output of fraction2date
        """

        expected = {
            0.5 : '20150101120000',
            1.5 : '20150102120000',
            364 : '20151231000000',

        }

        for day in expected:
            calc_time = dates.fraction2date(day)
            time = dates.format_inline_time(expected[day])

            self.assertTrue(
                calc_time.month == time.month and
                calc_time.day == time.day and
                calc_time.hour == time.hour and
                calc_time.second == time.second,
                "{} != {}".format(calc_time, time)
            )
