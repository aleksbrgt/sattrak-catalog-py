from rest_framework import viewsets

from catalog.models import LaunchSite
from api.serializers import LaunchSiteSerializer

class LaunchSiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
        LaunchSite API class view
    """
    queryset = LaunchSite.objects.all()
    serializer_class = LaunchSiteSerializer