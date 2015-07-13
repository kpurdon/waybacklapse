import sys
import requests


class Wayback:

    search_api = 'http://web.archive.org/cdx/search/cdx'
    images_api = 'http://web.archive.org/web'
    url_format = '{wayback}/{timestamp}/{url}'

    def __init__(self, url, start_year, stop_year, collapse=4):
        self.url = url
        self.start_year = start_year
        self.stop_year = stop_year
        self.collapse = collapse

    def _set_payload(self):

        collapse_str = 'timestamp:{0}'.format(self.collapse)

        payload = {
            'url': self.url,
            'output': 'json',
            'fl': 'timestamp,original',
            'from': self.start_year,
            'to': self.stop_year,
            'collapse': collapse_str
        }

        return payload

    def _get_captures(self, payload):

        res = requests.get(self.search_api, params=payload)
        if res.status_code == 503:
            sys.tracebacklimit = 0
            raise Exception(('The Wayback Machine API is down.'
                             'Check http://web.archive.org/cdx/search/cdx for details.'))

        captures = res.json()

        return captures[1:]  # remove the field names record

    def _get_urls(self, captures):

        capture_urls = [
            [capture[0], self.url_format.format(wayback=self.images_api,
                                                timestamp=capture[0],
                                                url=capture[1])]
            for capture in captures]

        return capture_urls

    def search(self):

        print('Searching the Wayback Machine ...')
        payload = self._set_payload()
        captures = self._get_captures(payload)
        urls = self._get_urls(captures)

        return urls
