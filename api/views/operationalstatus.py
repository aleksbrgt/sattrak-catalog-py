from rest_framework import viewsets

from catalog.models import OperationalStatus
from api.serializers import OperationalStatusSerializer

class OperationalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
        OperationalSatus API class view
    """
    queryset = OperationalStatus.objects.all()
    serializer_class = OperationalStatusSerializer