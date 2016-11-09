from selenium import webdriver

import unittest
import json

class APITest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def is_correct_json(self, string):
        """
            Check if the string is a well formed json
        """
        try:
            json.loads(string)
        except ValueError:
            return False

        return True

    def test_can_access_api_root_json(self):

        # A client checks out the api
        self.browser.get('http://localhost:8000/api?format=json')

        json = self.browser.find_element_by_tag_name('pre').text
        # It checks if the response is JSON
        self.assertTrue(self.is_correct_json(json))

        needed_content = [
            'launchsite',
            'operationalstatus',
            'orbitalstatus',
            'catalogentry',
            'tle',
            'datasource',
        ]
        # It check if correct data is available
        for element in needed_content:
            self.assertIn('api/%s/?format=json' % element, json)

    def test_can_access_api_root_browsable(self):
        # A user checks out the browsable API
        self.browser.get('http://localhost:8000/api?format=api')

        # He checks the page's title
        self.assertIn('Api Root', self.browser.title)
        # He checks if the response is HTML
        self.assertIn('<body', self.browser.page_source)

        stripped = ''.join(self.browser.page_source.split())
        self.assertTrue(stripped.endswith('</html>'))

if __name__ == '__main__':
    unittest.main(warnings='ignore')
