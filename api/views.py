"""
    API views
"""

from datetime import datetime

from django.db.models import Q

from rest_framework import viewsets, pagination, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from catalog.models import LaunchSite, OperationalStatus, OrbitalStatus, Source, CatalogEntry, TLE
from fetcher.models import DataSource
from .serializers import  DataSourceSerializer, LaunchSiteSerializer, OperationalStatusSerializer, OrbitalStatusSerializer, SourceSerializer, CatalogEntrySerializer, TLESerializer
from .tools.compute import SatelliteComputation
from .tools import dates as dateutils

class StandardResultSetPagination(pagination.PageNumberPagination):
    """
        Pagination class used in views returning a lot of data
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LaunchSiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
        LaunchSite API class view
    """
    queryset = LaunchSite.objects.all()
    serializer_class = LaunchSiteSerializer

class OperationalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
        OperationalSatus API class view
    """
    queryset = OperationalStatus.objects.all()
    serializer_class = OperationalStatusSerializer

class OrbitalStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
        OrbitalStatus API class view
    """
    queryset = OrbitalStatus.objects.all()
    serializer_class = OrbitalStatusSerializer

class SourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
        Source API class view
    """
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

class CatalogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
        CatalogEntry API class views
    """
    queryset = CatalogEntry.objects.all()
    serializer_class = CatalogEntrySerializer
    pagination_class = StandardResultSetPagination

    @detail_route(methods=['get'])
    def data(self, request, pk=None):
        """
            View returning basic positionning data
        """

        entry = self.get_object()
        time = datetime.utcnow()
        given_time = request.GET.get('time', None)

        try:
            if given_time is not None:
                time = dateutils.format_inline_time(given_time)

            tle = TLE.objects.findByCatalogEntryAndTime(
                entry, time
            )

            data = SatelliteComputation(tle)
            data.set_observer_time(time)
            data.basic_compute()

            return Response({
                'data': {
                    'date': time,
                    'object': {
                        'name': entry.names,
                        'international_designator': entry.international_designator,
                    },
                    'tle': {
                        'set_number': tle.set_number,
                        'epoch_year': tle.epoch_year,
                        'epoch_day': tle.epoch_day,
                    },
                },
                'object_elevation': data.elevation,
                'object_latitude': data.latitude,
                'object_longitude': data.longitude,
                'object_velocity': data.velocity,
            })

        except IndexError:
            return Response(
                {'details': 'No TLE corresponding to the given date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as err:
            return Response(
                {'details': '{0}'.format(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

class TLEViewSet(viewsets.ReadOnlyModelViewSet):
    """
        TLE API class view
    """
    queryset = TLE.objects.all()
    serializer_class = TLESerializer
    pagination_class = StandardResultSetPagination

class DataSourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
        DataSource API class view
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
