from django.test import TestCase
from django.urls import reverse

import ephem

from catalog.models import TLE
from api.tools import SatelliteComputation

class SatelliteComputationTestCase(TestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_emptyConstructorRaisesCorrectException(self):
        try:
            SatelliteComputation()
            self.fail("SatelliteComputation() can take no parameter")
        except TypeError as e:
            self.assertEquals("tle parameter is missing", str(e))


    def test_constructorCanTakeAWellFormedTleParameter(self):
        try:
            SatelliteComputation(tle=TLE.objects.first())
        except TypeError:
            self.fail("SatelliteComputation() can't take a 'tle' parameter")

    def test_constructorThrowsCorrectExceptionIfTheParamIsNotATle(self):
        try:
            SatelliteComputation(tle=None)
            self.fail("SatelliteComputation() can take a non TLE parameter")
        except TypeError as e:
            self.assertEquals("tle must be of type TLE", str(e))

    def test_constructorThrowsCorrectExceptionIfTheTleIsInvalid(self):
        try:
            SatelliteComputation(tle=TLE())
            self.fail("SatelliteComputation() can take an empty TLE")
        except ValueError as e:
            self.assertEquals("invalid TLE", str(e))

    def test_observerPropertyExists(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        try:
            sc.observer
        except AttributeError:
            self.fail("observer attribute does not exist")

    def test_observerPropertyIsAPyEphemObserver(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        self.assertTrue(
            isinstance(sc.observer, ephem.Observer),
            "observer is not of type ephem.Observer"
        )

    def test_constantGExists(self):
        try:
            SatelliteComputation.G
        except AttributeError:
            self.fail("G constant does not exist")

    def test_constantGHasCorrecValue(self):
        self.assertEquals(SatelliteComputation.G, 6.67408e-11)


    def test_constantEARTH_MASSExists(self):
        try:
            SatelliteComputation.EARTH_MASS
        except AttributeError:
            self.fail("EARTH_MASS constant does not exist")

    def test_constantEARTH_MASSHasCorrecValue(self):
        self.assertEquals(SatelliteComputation.EARTH_MASS, 5.98e24)

    def test_calcOrbitalVelocityExists(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        try:
            sc._calc_orbital_velocity()
        except AttributeError:
            self.fail("method _calc_orbital_velocity does not exist")
        except TypeError:
            pass

    def test_calcOrbitalVelocityTakesAParameter(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        try:
            sc._calc_orbital_velocity(0)
        except TypeError:
            self.fail("method _calc_orbital_velocity must take a parameter")

    def test_calcOrbitalVelocityRaisesACorrectExceptionIfAltitudeIsNotANumber(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        try:
            sc._calc_orbital_velocity(None)
            self.fail("method _calc_orbital_velocity can't accept a non number")
        except TypeError as e:
            self.assertEquals("altitude must be a number", str(e))

    def test_calcOrbitalVelocityRaisesACorrectExceptionIfAltitudeIsNegative(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        try:
            sc._calc_orbital_velocity(-1)
            self.fail("method _calc_orbital_velocity can't accept a negaitive number")
        except ValueError as e:
            self.assertEquals("altitude must be positive", str(e))

    def test_calcOrbitalProducesCorrectOutput(self):
        expected_velocities = {
            100 : 7849.1108,
            200 : 7789.2220,
            300 : 7730.6834,
            400 : 7673.4451,
            1000 : 7354.8236,
            2000 : 6901.9526,
        }

        results = {
            100 : 0,
            200 : 0,
            300 : 0,
            400 : 0,
            1000 : 0,
            2000 : 0,
        }

        sc = SatelliteComputation(tle = TLE.objects.first())

        for km in expected_velocities:
            results[km] = round(sc._calc_orbital_velocity(km * 1000), 4)

        self.assertEquals(expected_velocities, results)


    def test_checkMethodComputeExists(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        # Put the observer on a fixed date to avoid the test to fail while
        # running tests after the TLE expires
        sc.observer.date = '2017/8/25 20:00:00'

        try:
            sc.compute()
        except AttributeError:
            self.fail("compute() method does not exist")

    def test_methodComputeOutputsDataAsDict(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        # Put the observer on a fixed date to avoid the test to fail while
        # running tests after the TLE expires
        sc.observer.date = '2017/8/25 20:00:00'

        data = sc.compute()

        self.assertTrue(isinstance(data, dict), "output is not a dict")

    def test_methodComputeOutputsWellFormedDict(self):
        sc = SatelliteComputation(tle = TLE.objects.first())

        # Put the observer on a fixed date to avoid the test to fail while
        # running tests after the TLE expires
        sc.observer.date = '2017/8/25 20:00:00'

        data = sc.compute()

        expected_keys = ['longitude', 'latitude', 'elevation', 'velocity']

        for key in expected_keys:
            self.assertIn(key, data)

    def test_methodComputOutputsPyEphemDataAndCorrectVelocity(self):
        expected_data = {
            'elevation' : 406818.65625,
            'latitude' : 49.48508595186298,
            'longitude' : -156.969959505129,
            'velocity' : 7669.588322702025,
        }

        sc = SatelliteComputation(tle = TLE.objects.first())

        # Put the observer on a fixed date to avoid the test to fail while
        # running tests after the TLE expires
        sc.observer.date = '2017/8/25 20:00:00'

        data = sc.compute()

        self.assertEquals(expected_data, data)





