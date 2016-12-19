import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api.views import LaunchSiteViewSet, OperationalStatusViewSet, OrbitalStatusViewSet, SourceViewSet, CatalogEntryViewSet, TLEViewSet, DataSourceViewSet


def is_correct_json(string):
    """
        Check if the string is a well formed json
    """
    try:
        json.loads(string)
    except ValueError:
        return False

    return True

class ApiGetTestCase(TestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_json_is_correct(self):
        """
            Test if basic GET views are returning a correctly formed JSON
        """

        elements = [
            'LaunchSite',
            'OperationalStatus',
            'OrbitalStatus',
            'Source',
            'CatalogEntry',
            'TLE',
            'DataSource',
        ]

        for element in elements:
            # Dynamicly instanciate the view class
            request = self.factory.get('/api/%s/?format=json' % element.lower())
            view_class = globals()['%sViewSet' % element]
            view = view_class.as_view({'get': 'list'})
            response = view(request).render()

            self.assertTrue(is_correct_json(response.content.decode('utf8')))

    def test_json_has_pagination(self):
        """
            Test if some views has a pagination system
        """

        elements = [
            'TLE',
            'CatalogEntry'
        ]

        for element in elements:
            # Dynamicly instanciate the view class
            request = self.factory.get('/api/%s/?format=json' % element.lower())
            view_class = globals()['%sViewSet' % element]
            view = view_class.as_view({'get': 'list'})
            response = view(request).render()
            json_data = response.content.decode('utf8')

            self.assertIn('"count":', json_data)
            self.assertIn('"next":', json_data)
            self.assertIn('"previous":', json_data)
            self.assertIn('"results":', json_data)
