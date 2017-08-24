import requests
import time
import tempfile
import dateutil.parser

from tqdm import tqdm
from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from fetcher.models import DataSource
from fetcher import tools

from catalog.models import CatalogEntry,LaunchSite, OrbitalStatus, \
                           OperationalStatus, Source

class Command(BaseCommand):
    help = 'Import SatCat from specified datasource'

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

        self.stdout.write(self.style.SUCCESS('Successfully imported catalog'))

    def process_system_name(self, system_name):
        """
            Finds and process a DataSource by its system name
        """
        if (system_name == "all"):
            sources = DataSource.objects.filter(type=DataSource.CATALOG)
        else:
            sources = DataSource.objects.filter(
                system_name=system_name,
                type=DataSource.CATALOG
            )

        if not len(sources):
            raise CommandError('DataSource "%s" does not exist' % system_name)

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
        parser = tools.SatcatParser()

        for line in tqdm(lines, desc="Inserting  ", total=len(lines)):
            data = parser.parse_line(line)
            self.update(data)

    def update(self, data):
        """
            Update a catalog entry
        """
        try:
            entry = CatalogEntry.objects.get(
                norad_catalog_number=data['norad_catalog_number']
            )
        except CatalogEntry.DoesNotExist:
            entry = CatalogEntry()
            entry.added = timezone.localtime(timezone.now())

        has_payload = False
        if data['has_payload'] == '*':
            has_payload = True

        launch_date = data['launch_date']
        if launch_date != None:
            launch_date = dateutil.parser.parse(launch_date)
            launch_date = timezone.make_aware(launch_date)

        decay_date = data['decay_date']
        if decay_date != None:
            decay_date = dateutil.parser.parse(decay_date)
            decay_date = timezone.make_aware(decay_date)

        owner = None
        try:
            owner = Source.objects.get(code=data['owner'])
        except Source.DoesNotExist:
            pass

        operational_status = None
        try:
            operational_status = OperationalStatus.objects.get(
                code=data['operational_status']
            )
        except OperationalStatus.DoesNotExist:
            pass

        orbital_status = None
        try:
            orbital_status = OrbitalStatus.objects.get(
                code=data['orbital_status']
            )
        except OrbitalStatus.DoesNotExist:
            pass

        launch_site = None
        try:
            launch_site = LaunchSite.objects.get(
                code=data['launch_site']
            )
        except LaunchSite.DoesNotExist:
            pass

        entry.international_designator = data['international_designator']
        entry.norad_catalog_number = data['norad_catalog_number']
        entry.names = data['names']
        entry.has_payload = has_payload
        entry.operational_status = operational_status
        entry.owner = owner
        entry.launch_date = launch_date
        entry.launch_site = launch_site
        entry.decay_date = decay_date
        entry.orbital_period = data['orbital_period']
        entry.inclination = data['inclination']
        entry.apogee = data['apogee']
        entry.perigee = data['perigee']
        entry.radar_cross_section = data['radar_cross_section']
        entry.orbital_status = orbital_status
        entry.updated = timezone.localtime(timezone.now())

        entry.save()

