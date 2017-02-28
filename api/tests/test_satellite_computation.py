from django.test import TestCase
from django.urls import reverse

from catalog.models import TLE
from api.tools.compute import SatelliteComputation

class SatelliteComputationTestCase(TestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_orbitalVelocity(self):
        """
            Test the velocity calculation
        """

        # Expected result per distance in km
        expected = {
            100 : 7849.1108,
            200 : 7789.2220,
            300 : 7730.6834,
            400 : 7673.4451,
            1000 : 7354.8236,
            2000 : 6901.9526,
        }

        # Instanciate a computation with a dummy tle
        comp = SatelliteComputation(TLE.objects.first())
        comp.basic_compute()

        for km in expected:
            comp.elevation = km * 1000
            result = round(comp._calc_orbital_velocity(), 4)

            self.assertEquals(result, expected[km])

