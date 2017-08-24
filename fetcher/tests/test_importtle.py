from datetime import datetime

from requests.exceptions import ConnectionError

from django.core.management import call_command, get_commands
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO
from django.utils.dateformat import format

from fetcher.models import DataSource

class ImportTleTestCase(TestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_importtleCommandExists(self):
        """
            Test if importtle command exists
        """
        self.assertIn('importtle', get_commands())

    def test_importtleHasMandatoryParameterDatasourceName(self):
        """
            Test if parameters are mandatory
        """
        try:
            call_command('importtle', stdout=StringIO())
            self.fail('No mandatory parameter')
        except CommandError:
            pass

    def test_importtleUpdatesDataSourceUpdateDate(self):
        """
            Test if parameters are mandatory
        """

        # Edit the DataSource to make sure the date must be updated
        datasource = DataSource.objects.get(system_name='tle_test')
        datasource.last_time_checked = timezone.make_aware(datetime(2000, 1, 1))
        datasource.save()

        timestamp = format(datasource.last_time_checked, 'U')

        try:
            call_command('importtle', 'tle_test', stdout=StringIO())
        except ConnectionError:
            pass

        datasource = DataSource.objects.get(system_name='tle_test')

        self.assertNotEquals(
            timestamp,
            format(datasource.last_time_checked, 'U')
        )
