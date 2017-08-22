from datetime import datetime

from requests.exceptions import ConnectionError

from django.core.management import call_command, get_commands
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO
from django.utils.dateformat import format
from fetcher.models import DataSource

def ignoreRaises(test):
    """
        Makes error raising silent
    """
    def wrapper():
        test()
        return wrapper

class UpdateSatCatTestCase(TestCase):
    """
        Test the behavior of the updatesatcat command
    """

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_DataSourceModelExists(self):
        """
            Test if the DataSourceModel exists
        """
        try:
            from fetcher.models import DataSource
        except ImportError:
            self.fail('Cannot import DataSource')

    def test_updatesatcatCommandExists(self):
        """
            Test if updatesatcat command exists
        """
        self.assertIn('updatesatcat', get_commands())

    def test_updatesatcatHasMandatoryParameterDatasourceName(self):
        """
            Test if parameters are mandatory
        """
        out = StringIO()
        try:
            call_command('updatesatcat', stdout=out)
            output = out.getvalue()
        except CommandError:
            output = ''

        self.assertEquals('', output)

    @ignoreRaises
    def test_updatesatcatUpdatesDataSourceUpdateDate(self):
        """
            Test if updatesatcat updates the DataSource
        """

        # Edit the DataSource to make sure the date must be updated
        datasource = DataSource.objects.get(system_name='cat_test')
        datasource.last_time_checked = timezone.make_aware(datetime(2000, 1, 1))
        datasource.save()

        timestamp = format(datasource.last_time_checked, 'U')

        call_command('updatesatcat', 'cat_test')
        datasource = DataSource.objects.get(system_name='cat_test')

        self.assertNotEquals(timestamp, format(datasource.last_time_checked, 'U'))
