import requests
import os
from subprocess import call


START_YEAR = 2010
STOP_YEAR = 2015
LAPSE_LEVEL = 'yearly'
SITE_URL = 'nsidc.org'

IMAGE_OUTPUT_DIRECTORY = os.path.join('.', 'staging', 'images')
WAYBACK_API_ENDPOINT = 'http://archive.org/wayback/available'

if LAPSE_LEVEL == 'monthly':
    image_urls = {}
    for year in range(START_YEAR, STOP_YEAR + 1):
        for month in range(1, 12 + 1):
            timestamp = '{0}{1:02d}15'.format(year, month)

            payload = {'url': SITE_URL, 'timestamp': timestamp}
            response = requests.get(WAYBACK_API_ENDPOINT, params=payload)
            result = response.json()

            if result['archived_snapshots']:
                image_url = result['archived_snapshots']['closest']['url']
                image_timestamp = result['archived_snapshots']['closest']['timestamp']
                image_urls[image_timestamp] = image_url

    for timestamp, image_url in image_urls.iteritems():
        output_fn = os.path.join(IMAGE_OUTPUT_DIRECTORY, '{0}.png'.format(timestamp))
        if not os.path.exists(output_fn):
            cmd = 'curl http://localhost:3000/?url={0} > {1}'.format(image_url, output_fn)
            call(cmd, shell=True)

    cmd = 'convert -delay 100 staging/images/*.png waybacklapse.gif'
    call(cmd, shell=True)

elif LAPSE_LEVEL == 'yearly':
    image_urls = {}
    for year in range(START_YEAR, STOP_YEAR + 1):
        timestamp = '{0}06'.format(year)

        payload = {'url': SITE_URL, 'timestamp': timestamp}
        response = requests.get(WAYBACK_API_ENDPOINT, params=payload)
        result = response.json()

        if result['archived_snapshots']:
            image_url = result['archived_snapshots']['closest']['url']
            image_timestamp = result['archived_snapshots']['closest']['timestamp']
            image_urls[image_timestamp] = image_url

    for timestamp, image_url in image_urls.iteritems():
        output_fn = os.path.join(IMAGE_OUTPUT_DIRECTORY, '{0}.png'.format(timestamp))
        print output_fn
        if not os.path.exists(output_fn):
            cmd = 'curl http://localhost:3000/?url={0} > {1}'.format(image_url, output_fn)
            call(cmd, shell=True)

    cmd = 'convert -delay 100 staging/images/*.png waybacklapse.gif'
    call(cmd, shell=True)


else:
    raise Exception('LAPSE_LEVEL MUST BE ONE OF [yearly|monthly]')
