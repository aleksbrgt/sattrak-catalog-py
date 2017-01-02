"""
    Tools for satellite related calculations
"""

import math
from datetime import datetime

import ephem

class SatelliteComputation():
    """
        Tools for satellite related computation
    """

    G = 6.67408e-11
    EARTH_MASS = 5.98e24

    def __init__(self, tle):
        """
            Constructor
        """
        self._observer = ephem.Observer()
        self._observer.lat = '0'
        self._observer.lon = '0'
        self._observer.elevation =0

        self._satellite = ephem.readtle(
                tle.first_line,
                tle.second_line,
                tle.third_line
            )

    def _calc_orbital_velocity(self):
        """
            Calculate the estimated velocity for a given elevation
        """
        r = self.elevation + ephem.earth_radius

        return math.sqrt((SatelliteComputation.G * SatelliteComputation.EARTH_MASS) / r)

    def set_observer_time(self, time):
        self._observer.date = time

    def set_observer_latitude(self, latitude):
        self._observer.lat = latitude

    def set_observer_longitude(self, longitude):
        self._observer.lon = longitude

    def set_observer_elevation(self, elevation):
        sefl._observer.elevatation = elevatation

    def basic_compute(self):
        """
            Compute basic data
        """
        self._satellite.compute(self._observer)

        self.longitude = math.degrees(self._satellite.sublong)
        self.latitude = math.degrees(self._satellite.sublat)
        self.elevation = self._satellite.elevation
        self.velocity = self._calc_orbital_velocity()


