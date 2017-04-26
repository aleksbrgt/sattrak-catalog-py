from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from catalog.models import CatalogEntry, TLE
from api.serializers import CatalogEntrySerializer, TLESerializer

from api.tools.compute import SatelliteComputation
from api.tools import dates as dateutils

from . import StandardResultSetPagination

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