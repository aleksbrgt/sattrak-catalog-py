from datetime import datetime

import django_filters
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import filters

from rest_framework_filters import backends

from catalog.models import CatalogEntry, TLE
from api.serializers import CatalogEntrySerializer, TLESerializer

from api.tools.compute import SatelliteComputation
from api.tools import dates as dateutils

from api.views import StandardResultSetPagination
from api.views import CatalogEntryFilter

class CatalogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
        CatalogEntry API class views
    """
    queryset = CatalogEntry.objects.all()
    serializer_class = CatalogEntrySerializer
    pagination_class = StandardResultSetPagination

    filter_backends = (
        backends.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filter_class = CatalogEntryFilter

    search_fields = (
        'international_designator',
        'norad_catalog_number',
        'names',
        'launch_date',
        'decay_date',
        'owner__code',
        'owner__description',
        'launch_site__code',
        'launch_site__description',
        'operational_status__description',
        'orbital_status__description',
    )


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
                {'detail': 'No TLE corresponding to the given date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError as err:
            return Response(
                {'detail': '{0}'.format(err)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['get'])
    def tle(self, request, pk=None):
        """
            Return a TLE matching the given time if any, otherwise the latest
            TLE is shown
        """

        entry = self.get_object()
        time = datetime.utcnow()
        given_time = request.GET.get('time', None)

        try:
            if given_time is not None:
                time = dateutils.format_inline_time(given_time)

            tle = TLE.objects.findByCatalogEntryAndTime(entry, time)
            serializer = TLESerializer(tle)

            return Response(serializer.data)

        except IndexError:
            return Response(
                {'detail': 'No TLE corresponding to the given date.'},
                status=status.HTTP_400_BAD_REQUEST
            )