"""
    API views
"""

from datetime import datetime

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

        # Get the corresponding CatalogEntry
        entry = self.get_object()

        given_time = request.GET.get('time', None)

        time = datetime.utcnow()
        if given_time is not None:
            time = datetime.strptime(given_time, '%Y/%m/%d %H:%M:%S')

        last_digits_year = str(time.year)[-2:]
        day_fraction = dateutils.get_days(time)

        tle = None
        try:
            # The closest TLE for the satellite is picked, the TLE is always
            # older than the requested time
            tle = TLE.objects.filter(
                epoch_year__lte=last_digits_year,
                epoch_day__lte=day_fraction,
                satellite_number=entry).order_by(
                    'epoch_year',
                    'epoch_day'
                )[0]

        except IndexError:
            return Response(
                {'details': 'No TLE corresponding to the given date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = SatelliteComputation(tle)
        data.set_observer_time(time)

        try:
            data.basic_compute()
            return Response({
                'elevation': data.elevation,
                'latitude': data.latitude,
                'longitude': data.longitude,
                'velocity': data.velocity
            })
        except ValueError as err:
            # PyEphem is restricting the range of validity of the TLEs
            return Response({'detail': '{0}'.format(err)},
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
