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
        self._observer.date = datetime.utcnow()

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


    def basic_compute(self):
        """
            Compute basic data
        """
        self._satellite.compute(self._observer)

        self.longitude = self._satellite.sublong
        self.latitude = self._satellite.sublat
        self.elevation = self._satellite.elevation
        self.velocity = self._calc_orbital_velocity()
