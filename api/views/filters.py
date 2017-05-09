import rest_framework_filters as filters

from catalog.models import CatalogEntry, OperationalStatus, Source, LaunchSite, OrbitalStatus

class OrbitalStatusFilter(filters.FilterSet):
    class Meta:
        model = OrbitalStatus
        fields = {
            'code': ['exact', 'in', 'startswith'],
            'description': ['exact', 'in', 'startswith'],
        }

class LaunchSiteFilter(filters.FilterSet):
    class Meta:
        model = LaunchSite
        fields = {
            'code': ['exact', 'in', 'startswith'],
            'description': ['exact', 'in', 'startswith'],
        }

class SourceFilter(filters.FilterSet):
    class Meta:
        model = Source
        fields = {
            'code': ['exact', 'in', 'startswith'],
            'description': ['exact', 'in', 'startswith'],
        }

class OperationalStatusFilter(filters.FilterSet):
    class Meta:
        model = OperationalStatus
        fields = {
            'code': ['exact', 'in', 'startswith'],
            'description': ['exact', 'in', 'startswith'],
        }

class CatalogEntryFilter(filters.FilterSet):

    op_status = filters.RelatedFilter(
        OperationalStatusFilter,
        name='operational_status',
        queryset=OperationalStatus.objects.all()
    )

    orbital_status = filters.RelatedFilter(
        OrbitalStatusFilter,
        name='orbital_status',
        queryset=OrbitalStatus.objects.all()
    )

    launch_site = filters.RelatedFilter(
        LaunchSiteFilter,
        name='launch_site',
        queryset=LaunchSite.objects.all()
    )

    owner = filters.RelatedFilter(
        SourceFilter,
        name='owner',
        queryset=Source.objects.all()
    )

    class Meta:
        model = CatalogEntry
        fields = {
            'international_designator': ['exact', 'in', 'startswith'],
            'norad_catalog_number': ['exact', 'in', 'startswith'],
            'names': ['exact', 'in', 'startswith'],
        }
