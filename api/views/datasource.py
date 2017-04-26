from rest_framework import viewsets

from fetcher.models import DataSource
from api.serializers import DataSourceSerializer

class DataSourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
        DataSource API class view
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
