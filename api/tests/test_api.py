import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIRequestFactory

from api.views import LaunchSiteViewSet, OperationalStatusViewSet, OrbitalStatusViewSet, SourceViewSet, CatalogEntryViewSet, TLEViewSet, DataSourceViewSet, ComputeView
from api.tools import SatelliteComputation, format_inline_time
from catalog.models import CatalogEntry, TLE

def is_correct_json(string):
    """
        Check if the string is a well formed json
    """
    if len(string) == 0:
        return False

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

    def test_jsonIsCorrect(self):
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
            request = self.factory.get('/api/v1/%s/?format=json' % element.lower())
            view_class = globals()['%sViewSet' % element]
            view = view_class.as_view({'get': 'list'})
            response = view(request).render()

            self.assertTrue(is_correct_json(response.content.decode('utf8')))

    def test_jsonHasPagination(self):
        """
            Test if some views has a pagination system
        """

        elements = [
            'TLE',
            'CatalogEntry'
        ]

        for element in elements:
            # Dynamicly instanciate the view class
            request = self.factory.get('/api/v1/%s/?format=json' % element.lower())
            view_class = globals()['%sViewSet' % element]
            view = view_class.as_view({'get': 'list'})
            response = view(request).render()
            json_data = response.content.decode('utf8')

            self.assertIn('"count":', json_data)
            self.assertIn('"next":', json_data)
            self.assertIn('"previous":', json_data)
            self.assertIn('"results":', json_data)

    def test_listingCatalogEntriesWithLimit(self):
        """
            Check if the limit parameter is working
        """
        expected_results = {
            '': 2,
            '?limit=1': 2,
        }

        for search, expected in expected_results.items():
            response = self.client.get(
                '/api/v1/catalogentry/{}'.format(search)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)
            result = json_data['count']

            self.assertEqual(result, expected)

    def test_listCatalogEntriesWithFilters(self):
        """
            Check if filters in urls are working
        """

        to_check_basic = {
            'has_payload': True,
            'has_payload': False,
        }

        to_check_child = {
            'owner': 'ISS',
            'owner': 'PRC',
            'launch_site': 'TYMSC',
            'launch_site': 'JSC',
            'operational_status': '+',
        }

        for field, value in to_check_basic.items():
            response = self.client.get(
                '/api/v1/catalogentry/?{}={}'.format(field, value)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)

            for result in json_data['results']:
                self.assertEqual(json_data['results'][0][field], value)

        for field, value in to_check_child.items():
            response = self.client.get(
                '/api/v1/catalogentry/?{}={}'.format(field, value)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)

            for result in json_data['results']:
                self.assertEqual(json_data['results'][0][field]['code'], value)

    def test_listCatalogEntriesWithSortFilters(self):
        """
            Check if filters in urls are working
        """
        expected_orders = {
            'launch_date': ['25544', '37820'],
            '-launch_date': ['37820', '25544'],
            'norad_catalog_number': ['25544', '37820'],
            '-norad_catalog_number': ['37820', '25544'],
        }

        for param, order in expected_orders.items():
            response = self.client.get(
                '/api/v1/catalogentry/?ordering={}'.format(param)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)

            for i in range(len(order)):
                self.assertEqual(
                    json_data['results'][i]['norad_catalog_number'],
                    order[i]
                )

    def test_listCatalogEntriesWithComplexFilters(self):
        """
            Check if the more complex filters are working
        """

        expected_results = {
            '?norad_catalog_number__in=25544%2C25545': ['25544'],
            '?norad_catalog_number__startswith=255': ['25544'],
            '?owner__description__startswith=international': ['25544'],
            '?owner__operational_status__startswith=Operational&international_designator__startswith=2011-': ['37820'],
        }

        for search, expected in expected_results.items():
            response = self.client.get(
                '/api/v1/catalogentry/{}'.format(search)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)['results']

            results = []

            for data in json_data:
                results.append(data['norad_catalog_number'])

            self.assertEqual(results, expected)

    def test_listCatalogEntriesWithSearchFilters(self):
        """
            Check if the search filter is working corrently
        """
        expected_results = {
            '25544': ['25544'],
            'zarya': ['25544'],
            'international+space+station': ['25544'],
            'china': ['37820'],
            'jiuquan': ['37820'],
            'tiangong': ['37820'],
            'operational': ['25544', '37820'],
            'earth+orbit': ['25544', '37820'],
        }

        for search, expected in expected_results.items():
            response = self.client.get(
                '/api/v1/catalogentry/?search={}'.format(search)
            )
            content = response.content.decode('utf8')
            json_data = json.loads(content)['results']

            results = []

            for data in json_data:
                results.append(data['norad_catalog_number'])

            self.assertEqual(results, expected)

class ComputationTestCase(ApiGetTestCase):
    """
        Tests on the computation part of the api
    """

    fixtures = [
        'initial_data',
        'test_data',
    ]

    def test_computeViewExists(self):
        try:
            from api.views import ComputeView
        except ImportError:
            self.fail("Compute view does not exist")

    def test_computeRouteExists(self):
        """
            Check if the route is working
        """
        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')
        self.assertEquals(response.status_code, status.HTTP_200_OK)


    def test_computeRouteOnlyMatchesDigits(self):
        """
            Check if the route only matches digits in its parameter
        """
        response = self.client.get('/api/v1/compute/notadigit/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_computeRouteReturns404IfCatalogEntryDoesNotExist(self):
        """
            Check if a non existent satellite number outputs a 404 error
        """
        response = self.client.get('/api/v1/compute/0101/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_computeViewReturnsJsonData(self):
        """
            Check if the data returned by the view is json
        """
        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')

        self.assertTrue(
            is_correct_json(response.content.decode('utf8')),
            "compute view does not return json"
        )

    def test_computeViewReturnsExpectedJsonFormat(self):
        """
            Check if the returned json has the correct structure
        """
        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')
        content = response.content.decode('utf8')

        expected_keys = [
            'longitude',
            'latitude',
            'elevation',
            'velocity',
            'tle',
        ]

        json_data = json.loads(content)
        json_keys = [key for key in crawl_json(json_data)]


        for key in expected_keys:
            self.assertTrue(
                key in json_keys,
                "there is no key '{}' in the json".format(key)
            )

    def test_computeViewReturnsExpectedValueFormat(self):
        """
            Check if the returned json has the correct value types
        """
        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')
        content = response.content.decode('utf8')
        json_data = json.loads(content)

        for key in json_data:
            try:
                float(json_data[key])
            except ValueError:
                self.fail("{} is not a number".format(key))

    def test_computeViewReturnsSameDataAsSatelliteComputation(self):
        """
            Check if the view returns the same data as SatelliteComputation tool
        """
        tle = TLE.objects.findByCatalogEntryAndTime(
            CatalogEntry.objects.first(),
            format_inline_time('20170825200000')
        )
        sc = SatelliteComputation(tle = tle)

        # Put the observer on a fixed date to avoid the test to fail while
        # running after the TLE expires
        sc.observer.date = '2017/8/25 20:00:00'
        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')

        content = response.content.decode('utf8')
        json_data = json.loads(content)
        del json_data['tle']

        expected_data = sc.compute()

        self.assertEquals(json_data, expected_data)

    def test_computeViewReturnsCorrectDataAccordingToTheDate(self):
        """
            Check if the view returns the correct data according to the date
        """
        tle = TLE.objects.findByCatalogEntryAndTime(
            CatalogEntry.objects.first(),
            format_inline_time('20170825200000')
        )
        sc = SatelliteComputation(tle=tle)

        sc.observer.date = '2017/8/25 20:00:00'
        expected_data_1 = sc.compute()

        sc.observer.date = '2017/8/25 20:00:01'
        expected_data_2 = sc.compute()

        response = self.client.get('/api/v1/compute/25544/?time=20170825200000')
        content = response.content.decode('utf8')
        json_data_1 = json.loads(content)
        del json_data_1['tle']

        response = self.client.get('/api/v1/compute/25544/?time=20170825200001')
        content = response.content.decode('utf8')
        json_data_2 = json.loads(content)
        del json_data_2['tle']

        self.assertEquals(json_data_1, expected_data_1)
        self.assertEquals(json_data_2, expected_data_2)

    def test_computeViewReturns400IfTimeTooFarAway(self):
        """
            Check if the view returns an error 400 if the given time too far away
        """
        response = self.client.get('/api/v1/compute/25544/?time=20200825200000')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_computeViewReturns400IfNoTLEFoundForTime(self):
        """
            Check if the view returns an error 400 if no TLE is found for the
            given time
        """
        response = self.client.get('/api/v1/compute/25544/?time=200008252000001')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_getTLEFromCatalogEntryIsReachable(self):
        """
            Check if the request returns a correct JSON
        """
        response = self.client.get('/api/v1/catalogentry/25544/tle/?time=20170825200000')
        content = response.content.decode('utf8')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(content)
        self.assertTrue(is_correct_json(content))

    def test_getTLEFromCatalogEntryHasTLE(self):
        """
            Check if the request returns a TLE
        """
        response = self.client.get('/api/v1/catalogentry/25544/tle/?time=20170825200000')
        content = response.content.decode('utf8')
        json_data = json.loads(content)

        expected_data = {
            'id': 4,
            'first_line': 'ISS (ZARYA)',
            'second_line': '1 25544U 98067A   17059.83075553  .00002893  00000-0  50327-4 0  9991',
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in expected_data.items():
            self.assertTrue(key in json_data)
            self.assertEqual(json_data[key], value)

    def test_getTLEFromCatalogEntryReturns400IfNoTLEFoundForTime(self):
        """
            Check if the view returns an error 400 if not TLE is found for
            the given time
        """
        response = self.client.get('/api/v1/catalogentry/25544/tle/?time=20000825200000')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)