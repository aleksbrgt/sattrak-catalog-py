import requests
import time
import tempfile
import dateutil.parser

from hurry.filesize import size
from tqdm import tqdm
from django.db import transaction
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from fetcher.models import DataSource
from fetcher.tools import SatcatParser

from catalog.models import CatalogEntry, LaunchSite, OrbitalStatus, OperationalStatus, Source

class Command(BaseCommand):
    help = 'Update the satellite catalog'

    def add_arguments(self, parser):
        parser.add_argument('system_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for system_name in options['system_name']:
            self.process_system_name(system_name)

        self.stdout.write(self.style.SUCCESS('Successfully updated catalog entries'))

    def process_system_name(self, system_name):
        try:
            source = DataSource.objects.get(system_name=system_name)

            data = self.download(source.url)
            self.parse(data.splitlines())

            source.last_time_checked = timezone.now()
            source.save()

        except(DataSource.DoesNotExist):
            raise CommandError('DataSource "%s" does not exist' % system_name)

    def download(self, url):
        self.stdout.write(url)

        r = requests.head(url)
        r.raise_for_status()
        content_size = int(r.headers['content-length'])

        r = requests.get(url, stream=True)

        with tqdm(desc="Downloading", total=content_size, unit='B', unit_scale=True) as t:
            with tempfile.TemporaryFile() as temp:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        temp.write(chunk)
                        t.update(len(chunk))
                temp.seek(0)
                return temp.read()

        raise CommandError("File could not be downloaded")

    @transaction.atomic
    def parse(self, lines):
        parser = SatcatParser()

        for line in tqdm(lines, desc="Inserting  ", total=len(lines)):
            data = parser.parse_line(line)
            self.update(data)

    def update(self, data):
        try:
            entry = CatalogEntry.objects.get(norad_catalog_number=data['norad_catalog_number'])
        except CatalogEntry.DoesNotExist:
            entry = CatalogEntry()

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
            operational_status = OperationalStatus.objects.get(code=data['operational_status'])
        except OperationalStatus.DoesNotExist:
            pass

        orbital_status = None
        try:
            orbital_status = OrbitalStatus.objects.get(code=data['orbital_status'])
        except OrbitalStatus.DoesNotExist:
            pass

        launch_site = None
        try:
            launch_site = LaunchSite.objects.get(code=data['launch_site'])
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

        entry.save()

