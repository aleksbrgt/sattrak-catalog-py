from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from catalog.models import CatalogEntry, TLE
from api.tools import SatelliteComputation, format_inline_time

class ComputeView(APIView):

    def get(self, request, satellite_number, format=None):
        entry = get_object_or_404(
            CatalogEntry,
            norad_catalog_number=satellite_number
        )

        try:
            time = format_inline_time(request.GET.get('time', None))
        except ValueError:
            return Response(
                {'detail': 'The given time is not correct'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            tle = TLE.objects.findByCatalogEntryAndTime(entry, time)
        except:
            return Response(
                {'detail': 'No TLE corresponding to the given date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sc = SatelliteComputation(tle=tle)
        sc.observer.date = time

        try:
            data = sc.compute()
        except ValueError as e:
            return Response(
                {'detail': '{0}'.format(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'longitude' : data['longitude'],
            'latitude' : data['latitude'],
            'elevation' : data['elevation'],
            'velocity' : data['velocity'],
            'tle' : tle.id,
        })
