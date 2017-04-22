from django.db import models

class OperationalStatus(models.Model):

    class Meta:
        verbose_name_plural = "Operational statuses"

    code = models.CharField(
        max_length=1,
        primary_key=True
    )
    description = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.code
