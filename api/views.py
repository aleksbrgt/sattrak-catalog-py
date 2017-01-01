from rest_framework import viewsets, pagination

from catalog.models import LaunchSite, OperationalStatus, OrbitalStatus, Source, CatalogEntry, TLE
from fetcher.models import DataSource
from .serializers import  DataSourceSerializer, LaunchSiteSerializer, OperationalStatusSerializer, OrbitalStatusSerializer, SourceSerializer, CatalogEntrySerializer, TLESerializer

class StandardResultSetPagination(pagination.PageNumberPagination):
    """
        Pagination class used in views returning a lot of data
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LaunchSiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LaunchSite.objects.all()
    serializer_class = LaunchSiteSerializer

class OperationalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OperationalStatus.objects.all()
    serializer_class = OperationalStatusSerializer

class OrbitalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrbitalStatus.objects.all()
    serializer_class = OrbitalStatusSerializer

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class CatalogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogEntry.objects.all()
    serializer_class = CatalogEntrySerializer
    pagination_class = StandardResultSetPagination

class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TLE.objects.all()
    serializer_class = TLESerializer
    pagination_class = StandardResultSetPagination

class DataSourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
