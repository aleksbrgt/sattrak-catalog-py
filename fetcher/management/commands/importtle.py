from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from tqdm import tqdm

from fetcher import tools
from fetcher.models import DataSource
from catalog.models import CatalogEntry, TLE

class Command(BaseCommand):
    help = 'Import TLE from specified datasource'

    def add_arguments(self, parser):
        """
            Set command's arguments
        """
        parser.add_argument('system_name', nargs='+', type=str)

    def handle(self, *args, **options):
        """
            Main function
        """
        for system_name in options['system_name']:
            self.process_system_name(system_name)

        self.stdout.write(self.style.SUCCESS('Successfully imported TLEs'))

    def process_system_name(self, system_name):
        """
            Finds and process a DataSource by its system name
        """
        if (system_name == "all"):
            sources = DataSource.objects.filter(type=DataSource.TLE)
        else:
            sources = DataSource.objects.filter(
                type=DataSource.TLE,
                system_name=system_name
            )

        if not len(sources):
            raise CommandError('DataSource "%s" does not exists' % system_name)

        for source in sources:
            source.last_time_checked = timezone.now()
            source.save()

            self.stdout.write(source.url)
            data = tools.download(source.url)
            if (data == False):
                raise CommandError("File could not be downloaded")

            self.parse(data.splitlines())

    @transaction.atomic
    def parse(self, lines):
        """
            Loop through received file and parse its content
        """
        parser = tools.TleParser()

        group = {}
        for line in tqdm(lines, desc="Inserting  ", total=len(lines)):
            group[len(group)] = line
            if len(group) == 3:
                self.update(parser.parse(group))
                group = {}

    def update(self, data):
        """
            Insert a TLE
        """
        try:
            catalogEntry = CatalogEntry.objects.get(
                norad_catalog_number=data['satellite_number']
            )
        except CatalogEntry.DoesNotExist:
            # Do not insert the TLE if the catalog entry it makes reference to
            # does not exist
            return False

        try:
            tle = TLE.objects.get(
                first_line=data['line_0_full'],
                second_line=data['line_1_full'],
                third_line=data['line_2_full'],
            )
            # Do not go further if the TLE already is in the database
            return False
        except TLE.DoesNotExist:
            pass

        tle = TLE()

        tle.first_line = data['line_0_full']
        tle.second_line = data['line_1_full']
        tle.third_line = data['line_2_full']
        tle.satellite_number = catalogEntry
        tle.classificatoin = data['classification']
        tle.international_designator_year = data['international_designator_year']
        tle.international_designator_number = data['international_designator_number']
        tle.international_designator_piece = data['international_designator_piece']
        tle.epoch_year = data['epoch_year']
        tle.epoch_year = data['epoch_year']
        tle.epoch_day = data['epoch_day']
        tle.first_derivative_mean_motion = data['first_derivative_mean_motion']
        tle.second_derivative_mean_motion = data['second_derivative_mean_motion']
        tle.drag = data['drag']
        tle.set_number = data['set_number']
        tle.first_checksum = data['first_checksum']
        tle.inclination = data['inclination']
        tle.ascending_node = data['ascending_node']
        tle.eccentricity = data['eccentricity']
        tle.perigee_argument = data['perigee_argument']
        tle.mean_anomaly = data['mean_anomaly']
        tle.mean_motion = data['mean_motion']
        tle.revolution_number = data['revolution_number']
        tle.second_checksum = data['second_checksum']
        tle.added = timezone.localtime(timezone.now())

        tle.save()


