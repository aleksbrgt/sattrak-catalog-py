from rest_framework import viewsets

from catalog.models import Source
from api.serializers import SourceSerializer

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Source API class view
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
