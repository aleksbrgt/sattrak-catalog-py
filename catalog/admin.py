from django.contrib import admin
from .models import LaunchSite, OperationalStatus, OrbitalStatus, Source, CatalogEntry, TLE

admin.site.register(LaunchSite)
admin.site.register(OperationalStatus)
admin.site.register(OrbitalStatus)
admin.site.register(Source)
admin.site.register(CatalogEntry)
admin.site.register(TLE)