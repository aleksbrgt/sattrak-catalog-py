from datetime import datetime

from requests.exceptions import ConnectionError

from django.test import TestCase

from fetcher.tools import SatcatParser

class SatcatParserTestCase(TestCase):
    """
        Test the behavior of the SatcatParser tool
    """

    def test_canImportSatcatparser(self):
        """
            Test if SatcatParser exists
        """
        try:
            from fetcher.tools import SatcatParser
        except ImportError:
            self.fail('Cannot import SatcatParser')

    def test_defaultFormatIsCelesTrak(self):
        """
            Test if the default format is CelesTrak
        """
        parser = SatcatParser()
        self.assertEquals(SatcatParser.CELESTRAK, parser.format)

    def test_explodeWorksInSimpleCase(self):
        """
            Test if SatcatParser parses data correctly
        """
        line = "1957-001A    00001   D SL-1 R/B                  CIS    1957-10-04  TYMSC  1957-12-01     96.2   65.1     938     214   20.4200     "

        expected = {
            'international_designator': '1957-001A',
            'norad_catalog_number': '00001',
            'multiple_flag': None,
            'has_payload': None,
            'operational_status': 'D',
            'names': 'SL-1 R/B',
            'owner': 'CIS',
            'launch_date': '1957-10-04',
            'launch_site': 'TYMSC',
            'decay_date': '1957-12-01',
            'orbital_period': '96.2',
            'inclination': '65.1',
            'apogee': '938',
            'perigee': '214',
            'radar_cross_section': '20.4200',
            'orbital_status': None,
        }


        parser = SatcatParser()
        data = parser.explode(line)

        for key in expected:
            self.assertEquals(expected[key], data[key])

    def test_parserChecksForInvalidValues(self):
        """
            Test if SatcatParser checks for invalid values
        """
        line = "1957-001A    00001   D SL-1 R/B                  CIS    1957-10-04  TYMSC  1957-12-01     96.2   65.1     938     214   N/A     "

        expected = {
            'international_designator': '1957-001A',
            'norad_catalog_number': '00001',
            'multiple_flag': None,
            'has_payload': None,
            'operational_status': 'D',
            'names': 'SL-1 R/B',
            'owner': 'CIS',
            'launch_date': '1957-10-04',
            'launch_site': 'TYMSC',
            'decay_date': '1957-12-01',
            'orbital_period': '96.2',
            'inclination': '65.1',
            'apogee': '938',
            'perigee': '214',
            'radar_cross_section': None,
            'orbital_status': None,
        }

        parser = SatcatParser()
        data = parser.explode(line)

        for key in expected:
            self.assertEquals(expected[key], data[key])
