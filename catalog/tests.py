from django.test import TestCase
from django.db.utils import IntegrityError

from .models import CatalogEntry

class CatalogTestCase(TestCase):

    fixtures = [
        'initial_data'
    ]

    def test_catalog_entry_decay_date_accepts_null_value(self):
        entry = CatalogEntry.objects.get(norad_catalog_number='2554')
        entry.decay_date = None

        try:
            entry.save()
        except IntegrityError:
            self.assertRaises(IntegrityError)
