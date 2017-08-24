from django.test import TestCase

class FetcherTestCase(TestCase):

    def test_DataSourceModelExists(self):
        """
            Test if DataSource model exists
        """
        try:
            from fetcher.models import DataSource
        except ImportError:
            self.fail('Cannot import DataSource')
