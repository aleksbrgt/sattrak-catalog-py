from django.db import models

class LaunchSite(models.Model):

    code = models.CharField(
        max_length=20,
        primary_key=True
    )
    description = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.code
