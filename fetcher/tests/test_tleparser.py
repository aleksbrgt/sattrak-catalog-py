from datetime import datetime

from requests.exceptions import ConnectionError

from django.test import TestCase

from fetcher.tools import TleParser

class TleParserTestCase(TestCase):
    """
        Test the behavior of the TleParser tool
    """

    def test_canImportTlecatparser(self):
        """
            Test if TleParser exists
        """
        try:
            from fetcher.tools import TleParser
        except ImportError:
            self.fail('Cannot import TleParser')

    def test_defaultFormatIsCelesTrak(self):
        """
            Test if the default format is CelesTrak
        """
        parser = TleParser()
        self.assertEquals(TleParser.CELESTRAK, parser.format)

    def test_explodeWorksInSimpleCase(self):
        """
            Test if TleParser parses data correctly
        """
        lines = [
            'ISS (ZARYA)             ',
            '1 25544U 98067A   17236.53358279  .00001862  00000-0  35301-4 0  9994',
            '2 25544  51.6396  57.6070 0005086 172.6034 285.4459 15.54193317 72385',
        ]

        expected = {
            'line_0_full': 'ISS (ZARYA)',
            'name': 'ISS (ZARYA)',
            'line_1_full': '1 25544U 98067A   17236.53358279  .00001862  00000-0  35301-4 0  9994',
            'line_number': '1',
            'satellite_number': '25544',
            'classification': 'U',
            'international_designator_year': '98',
            'international_designator_number': '067',
            'international_designator_piece': 'A',
            'epoch_year': '17',
            'epoch_day': '236.53358279',
            'first_derivative_mean_motion': '0.00001862',
            'second_derivative_mean_motion': '0',
            'drag': 0.00035301,
            'set_number': '999',
            'first_checksum': '4',
            'line_2_full': '2 25544  51.6396  57.6070 0005086 172.6034 285.4459 15.54193317 72385',
            'inclination': '51.6396',
            'ascending_node': '57.6070',
            'eccentricity': '0.0005086',
            'perigee_argument': '172.6034',
            'mean_anomaly': '285.4459',
            'mean_motion': '15.54193317',
            'revolution_number': '7238',
            'second_checksum': '5',
        }

        parser = TleParser()
        data = parser.explode(lines)

        for n in expected:
            self.assertEquals(expected[n], data[n], n)

    def test_explodeWorksWhenNoDrag(self):
        """
            Test if TleParser parses data correctly when there is no drag
        """
        lines = [
            'GOES 13                 ',
            '1 29155U 06018A   17236.28392374 -.00000277  00000-0  00000+0 0  9990',
            '2 29155   0.0320 231.9245 0003315 245.6473 242.4487  1.00264274 41246',
        ]

        expected = {
            'line_0_full': 'GOES 13',
            'name': 'GOES 13',
            'line_1_full': '1 29155U 06018A   17236.28392374 -.00000277  00000-0  00000+0 0  9990',
            'line_number': '1',
            'satellite_number': '29155',
            'classification': 'U',
            'international_designator_year': '06',
            'international_designator_number': '018',
            'international_designator_piece': 'A',
            'epoch_year': '17',
            'epoch_day': '236.28392374',
            'first_derivative_mean_motion': '0.00000277',
            'second_derivative_mean_motion': '0',
            'drag': 0,
            'set_number': '999',
            'first_checksum': '0',
            'line_2_full': '2 29155   0.0320 231.9245 0003315 245.6473 242.4487  1.00264274 41246',
            'inclination': '0.0320',
            'ascending_node': '231.9245',
            'eccentricity': '0.0003315',
            'perigee_argument': '245.6473',
            'mean_anomaly': '242.4487',
            'mean_motion': '1.00264274',
            'revolution_number': '4124',
            'second_checksum': '6',
        }

        parser = TleParser()
        data = parser.explode(lines)

        for n in expected:
            self.assertEquals(expected[n], data[n], n)

    def test_format_drag_positive(self):
        """
            Test if the drag is correctly defined with a negative positive
        """

        value = "88849-3"
        expected = 0.0088849

        tle = TleParser()
        self.assertEquals(expected, tle.format_drag(value))

    def test_format_drag_negative(self):
        """
            Test if the drag is correctly defined with a negative positive
        """

        value = "-62555-3"
        expected = 0.0062555

        tle = TleParser()
        self.assertEquals(expected, tle.format_drag(value))

    def test_format_drag_zero(self):
        """
            Test if the drag is correctly defined with a negative positive
        """

        value = "00000+0"
        expected = 0

        tle = TleParser()
        self.assertEquals(expected, tle.format_drag(value))
