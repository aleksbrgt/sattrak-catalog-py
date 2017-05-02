import datetime
import pytz

from django.db import models
from catalog.models import TLE

class CatalogEntry(models.Model):

    class Meta:
        verbose_name_plural = "Catalog entries"

    international_designator = models.CharField(
        max_length=11,
        unique=True
    )
    norad_catalog_number = models.CharField(
        max_length=5,
        primary_key=True
    )
    names = models.CharField(max_length=255)
    has_payload = models.BooleanField(default=False)
    operational_status_code = models.ForeignKey(
        "OperationalStatus",
        models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        "Source",
        models.SET_NULL,
        blank=True,
        null=True
    )
    launch_date = models.DateTimeField()
    launch_site = models.ForeignKey(
        "LaunchSite",
        models.SET_NULL,
        blank=True,
        null=True
    )
    decay_date = models.DateTimeField(
        blank=True,
        null=True
    )
    orbital_period = models.PositiveIntegerField()
    inclination = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    apogee = models.PositiveIntegerField()
    perigee = models.PositiveIntegerField()
    radar_cross_section = models.DecimalField(
        max_digits=7,
        decimal_places=4
    )
    orbital_status_code = models.ForeignKey(
        "OrbitalStatus",
        models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.international_designator
