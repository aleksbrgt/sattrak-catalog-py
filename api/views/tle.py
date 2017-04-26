from rest_framework import viewsets

from catalog.models import TLE
from api.serializers import TLESerializer

from api.views import StandardResultSetPagination

class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    """
        TLE API class view
    """
    queryset = TLE.objects.all()
    serializer_class = TLESerializer
    pagination_class = StandardResultSetPagination