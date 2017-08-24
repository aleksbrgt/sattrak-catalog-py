from django.db import models
from catalog.managers import TLEManager

class TLE(models.Model):

    class Meta:
        verbose_name = "Two Line Element"
        verbose_name_plural = "Two Line Elements"

    first_line = models.CharField(
        max_length=70,
        null=True
    )
    second_line = models.CharField(
        max_length=70,
        null=True
    )
    third_line = models.CharField(
        max_length=70,
        default=""
    )

    satellite_number = models.ForeignKey(
        "CatalogEntry",
        models.SET_NULL,
        blank=True,
        null=True
    )
    classification = models.ForeignKey(
        "OperationalStatus",
        models.SET_NULL,
        blank=True,
        null=True
    )
    international_designator_year = models.CharField(
        max_length=2
    )
    international_designator_number = models.CharField(
        max_length=3
    )
    international_designator_piece = models.CharField(
        max_length=3
    )
    epoch_year = models.CharField(
        max_length=2
    )
    epoch_day = models.DecimalField(
        max_digits=11,
        decimal_places=8
    )
    first_derivative_mean_motion = models.DecimalField(
        max_digits=9,
        decimal_places=8
    )
    second_derivative_mean_motion = models.DecimalField(
        max_digits=9,
        decimal_places=8
    )
    drag = models.DecimalField(
        max_digits=10,
        decimal_places=9
    )
    set_number = models.PositiveIntegerField()
    first_checksum = models.PositiveSmallIntegerField()

    inclination = models.DecimalField(
        max_digits=7,
        decimal_places=4
    )
    ascending_node = models.DecimalField(
        max_digits=7,
        decimal_places=4
    )
    eccentricity = models.DecimalField(
        max_digits=8,
        decimal_places=7
    )
    perigee_argument = models.DecimalField(
        max_digits=7,
        decimal_places=4
    )
    mean_anomaly = models.DecimalField(
        max_digits=7,
        decimal_places=4
    )
    mean_motion = models.DecimalField(
        max_digits=10,
        decimal_places=8
    )
    revolution_number = models.PositiveIntegerField()
    second_checksum = models.PositiveSmallIntegerField()
    added = models.DateTimeField(
        null=True
    )

    objects = TLEManager()

    def __str__(self):
        return '%s:%i' % (self.satellite_number.international_designator , self.set_number)
