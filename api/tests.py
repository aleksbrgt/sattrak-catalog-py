import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.views import LaunchSiteViewSet, OperationalStatusViewSet, OrbitalStatusViewSet, SourceViewSet, CatalogEntryViewSet, TLEViewSet, DataSourceViewSet


def is_correct_json(string):
    """
        Check if the string is a well formed json
    """
    if string[0] is not '{' and string[0] is not '[':
        return False

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

class ComputationTestCase(ApiGetTestCase):

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_access_data(self):
        response = self.client.get('/api/catalogentry/2554/data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_data(self):
        response = self.client.get('/api/catalogentry/2554/data/')
        content = response.content.decode('utf8')
        expected_data = [
            'elevation',
            'longitude',
            'latitude',
            'velocity',
        ]

        self.assertTrue(is_correct_json(content))

        json_data = json.loads(content)

        for key in expected_data:
            self.assertTrue(key in json_data)
