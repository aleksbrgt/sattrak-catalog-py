from django.db import models

class DataSource(models.Model):

    CATALOG = 'CAT'
    TLE = 'TLE'
    TYPE_CHOICES = (
        (CATALOG, 'Catalog'),
        (TLE, 'Two Line Elements')
    )

    type = models.CharField(
        max_length = 3,
        choices = TYPE_CHOICES,
        default = CATALOG
    )
    name = models.CharField(
        max_length=255
    )
    url = models.CharField(
        max_length=255
    )
    comment = models.TextField()
    date_added = models.DateTimeField()
    last_time_checked = models.DateTimeField()
    