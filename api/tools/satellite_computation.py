"""
    Tools for satellite related calculations
"""

import math

import ephem


from catalog.models import TLE

class SatelliteComputation(object):
    """
        Tools for satellite related computation
    """

    G = 6.67408e-11
    EARTH_MASS = 5.98e24

    def __init__(self, **kwargs):
        self.observer = ephem.Observer()
        self._satellite = None

        if 'tle' not in kwargs:
            raise TypeError("tle parameter is missing")

        tle = kwargs['tle']
        if type(tle) is not TLE:
            raise TypeError("tle must be of type TLE")

        try:
            self._satellite = ephem.readtle(
                tle.first_line,
                tle.second_line,
                tle.third_line
            )
        except TypeError:
            raise ValueError("invalid TLE")

    def _calc_orbital_velocity(self, altitude):
        try:
            float(altitude)
        except:
            raise TypeError("altitude must be a number")

        if altitude < 0:
            raise ValueError("altitude must be positive")

        r = altitude + ephem.earth_radius

        return math.sqrt((SatelliteComputation.G * SatelliteComputation.EARTH_MASS) / r)


    def compute(self):
        self._satellite.compute(self.observer)
        return {
            'longitude' : math.degrees(self._satellite.sublong),
            'latitude' : math.degrees(self._satellite.sublat),
            'elevation' : self._satellite.elevation,
            'velocity' : self._calc_orbital_velocity(self._satellite.elevation),
        }