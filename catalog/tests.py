import datetime
import pytz

from django.test import TestCase
from django.db.utils import IntegrityError

from .models import CatalogEntry, TLE

class CatalogTestCase(TestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_catalogEntryDecayDateAcceptsNullValue(self):
        entry = CatalogEntry.objects.get(norad_catalog_number='25544')
        entry.decay_date = None

        try:
            entry.save()
        except IntegrityError:
            self.assertRaises(IntegrityError)

    def test_tleHasThirdLineAttribute(self):
        self.assertTrue(hasattr(TLE, 'third_line'))

    def test_tleHasDateAddedAttribute(self):
        self.assertTrue(hasattr(TLE, 'date_added'))

    def test_getValidTLEReturnsCorrectTLE(self):
        entry = CatalogEntry.objects.get(norad_catalog_number='25544')

        time1 = datetime.datetime(2016, 12, 1, 8, 0, 0, tzinfo=pytz.UTC)
        time2 = datetime.datetime(2017, 3, 28, 14, 0, 0, tzinfo=pytz.UTC)

        expected_tle_1 = TLE.objects.get(id=1)
        expected_tle_2 = TLE.objects.get(id=3)

        self.assertTrue(expected_tle_1, entry.getValidTLE(time1))
        self.assertTrue(expected_tle_2, entry.getValidTLE(time2))
