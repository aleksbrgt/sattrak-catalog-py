from django.test import TestCase

class FetcherTestCase(TestCase):

    def test_DataSourceModelExists(self):
        try:
            from .models import DataSource
        except ImportError:
            self.fail('Cannot import DataSource')
