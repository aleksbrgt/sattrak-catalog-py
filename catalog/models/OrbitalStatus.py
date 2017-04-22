from django.db import models

class OrbitalStatus(models.Model):

    class Meta:
        verbose_name_plural = "Orbital statuses"

    code = models.CharField(
        max_length=3,
        primary_key=True
    )
    description = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.code
