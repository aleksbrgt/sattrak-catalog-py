from django.db import models

import datetime
import pytz

class TLEManager(models.Manager):

    def findByCatalogEntryAndTime(self, catalogEntry, time = None):
        """
            Return a tle matching the given time and catalog entry
        """
        if time is None:
            time = datetime.utcnow()

        time = time.replace(tzinfo=pytz.UTC)

        tles = self.filter(
                models.Q(
                    added__lte=time
                ),
                satellite_number=catalogEntry
            ).order_by(
                '-added',
            )

        if tles.exists():
            return tles[0]

        raise IndexError("No TLE found for the given time")
