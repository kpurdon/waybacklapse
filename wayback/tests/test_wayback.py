import unittest
import httpretty

import wayback.wayback as wayback


class TestWayback(unittest.TestCase):

    def setUp(self):
        self.wb = wayback.Wayback('foo', 2, '1996', '2015', 4)
        self.payload = {
            'url': 'foo',
            'limit': 2,
            'output': 'json',
            'fl': 'timestamp,original',
            'from': '1996',
            'to': '2015',
            'collapse': 'timestamp:4'
        }
        self.captures = [['123', 'foo'], ['456', 'bar']]
        self.urls = [['123', 'http://web.archive.org/web/123/foo'],
                     ['456', 'http://web.archive.org/web/456/bar']]
        self.body = '[["timestamp","original"],["123","foo"],["456","bar"]]'

    def test_set_payload(self):
        """
        The payload is set correctly
        """
        actual = self.wb._set_payload()
        self.assertDictEqual(self.payload, actual)

    @httpretty.activate
    def test_get_captures(self):
        """
        Wayback cdx response (captures) are processed correctly
        """
        httpretty.register_uri(httpretty.GET, self.wb.search_api, body=self.body,
                               content_type="application/json")

        actual = self.wb._get_captures(self.payload)
        self.assertEqual(self.captures, actual)

    def test_get_urls(self):
        """
        Captures are correclty processed into urls
        """
        actual = self.wb._get_urls(self.captures)
        self.assertEqual(self.urls, actual)
