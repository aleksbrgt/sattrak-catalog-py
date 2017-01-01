from rest_framework import serializers

from catalog.models import LaunchSite, OperationalStatus, OrbitalStatus, Source, CatalogEntry, TLE
from fetcher.models import DataSource

class LaunchSiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LaunchSite
        fields = (
            'code',
            'description',
        )

class OperationalStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperationalStatus
        fields = (
            'code',
            'description',
        )

class OrbitalStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrbitalStatus
        fields = (
            'code',
            'description',
        )

class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = (
            'code',
            'description',
        )

class CatalogEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CatalogEntry
        fields = (
            'international_designator',
            'norad_catalog_number',
            'names',
            'has_payload',
            'operational_status_code',
            'owner',
            'launch_date',
            'launch_site',
            'decay_date',
            'orbital_period',
            'inclination',
            'apogee',
            'perigee',
            'radar_cross_section',
            'orbital_status_code',
        )

class TLESerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TLE
        fields = (
            'id',
            'first_line',
            'second_line',
            'third_line',
            'satellite_number',
            'classification',
            'international_designator_year',
            'international_designator_number',
            'international_designator_piece',
            'epoch_year',
            'epoch_day',
            'first_derivative_mean_motion',
            'second_derivative_mean_motion',
            'drag',
            'set_number',
            'first_checksum',
            'inclination',
            'ascending_node',
            'eccentricity',
            'perigee_argument',
            'mean_anomaly',
            'mean_motion',
            'revolution_number',
            'second_checksum',
        )

class DataSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSource
        fields = (
            'id',
            'type',
            'name',
            'url',
            'comment',
            'date_added',
            'last_time_checked',
        )
