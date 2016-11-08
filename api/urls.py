from django.conf.urls import url, include
from rest_framework import routers

from .views import LaunchSiteViewSet, OperationalStatusViewSet, OrbitalStatusViewSet, SourceViewSet, CatalogEntryViewSet, TLEViewSet, DataSourceViewSet

router = routers.DefaultRouter()
router.register(r'launchsite', LaunchSiteViewSet)
router.register(r'operationalstatus', OperationalStatusViewSet)
router.register(r'orbitalstatus', OrbitalStatusViewSet)
router.register(r'source', SourceViewSet)
router.register(r'catalogentry', CatalogEntryViewSet)
router.register(r'tle', TLEViewSet)
router.register(r'datasource', DataSourceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
