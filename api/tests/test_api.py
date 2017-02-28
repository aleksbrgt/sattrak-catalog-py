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

def crawl_json(json):
    """
        Retrieve all the keys in a json object
    """
    for key in json:
        if type(json[key]) is dict:
            for k in crawl_json(json[key]):
                yield k
        yield key

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
    """
        Tests on the computation part of the api
    """

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_access_data(self):
        """
            Check if the route is working
        """
        response = self.client.get('/api/catalogentry/2554/data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_data_has_data(self):
        """
            Check if the page contains basic data
        """
        response = self.client.get('/api/catalogentry/2554/data/')
        content = response.content.decode('utf8')
        expected_data = [
            'object_elevation',
            'object_longitude',
            'object_latitude',
            'object_velocity',
            'data',
            'date',
            'object',
            'name',
            'international_designator',
            'tle',
            'set_number',
            'epoch_year',
            'epoch_day',
        ]

        self.assertTrue(is_correct_json(content))

        json_data = json.loads(content)
        json_keys = [key for key in crawl_json(json_data)]

        for key in expected_data:
            self.assertTrue(key in json_keys, "{} is not present".format(key))

    def test_data_anterior_date(self):
        """
            Check if a query is not processed when the requested time is before
            the TLE
        """
        response = self.client.get('/api/catalogentry/2554/data/?time=20161109010000')
        content = response.content.decode('utf8')
        json_data = json.loads(content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(is_correct_json(content))
        self.assertTrue('details' in json_data)
        self.assertEqual(json_data['details'], 'No TLE corresponding to the given date')

    def test_data_out_of_range_date(self):
        """
            Check if a query is not processed when the requested time is too far
            away from the TLE
        """
        response = self.client.get('/api/catalogentry/2554/data/?time=21000101080000')
        content = response.content.decode('utf8')
        json_data = json.loads(content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(is_correct_json(content))
        self.assertTrue('details' in json_data)

