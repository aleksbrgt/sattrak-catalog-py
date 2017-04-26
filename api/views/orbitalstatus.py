from rest_framework import viewsets

from catalog.models import OrbitalStatus
from api.serializers import OrbitalStatusSerializer

class OrbitalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
        OrbitalStatus API class view
    """
    queryset = OrbitalStatus.objects.all()
    serializer_class = OrbitalStatusSerializer
