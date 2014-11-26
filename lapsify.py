import requests
import os
from subprocess import call


START_YEAR = 1998
STOP_YEAR = 2015
LAPSE_LEVEL = 'yearly'
LAPSE_SPEED = 75  # slow=200 medium=100 fast=50
SITE_URL = 'google.com'

IMAGE_OUTPUT_DIRECTORY = os.path.join('.', 'staging', 'images')
WAYBACK_API_ENDPOINT = 'http://web.archive.org/cdx/search/cdx'
WAYBACK_URL_ENDPOINT = 'http://web.archive.org/web'

call('mkdir -p {0}'.format(IMAGE_OUTPUT_DIRECTORY), shell=True)

collapse = {'yearly': 'timestamp:4', 'monthly': 'timestamp:6'}

payload = {
    'url': SITE_URL,
    'output': 'json',
    'fl': 'timestamp,original',
    'from': START_YEAR,
    'to': STOP_YEAR,
    'collapse': collapse[LAPSE_LEVEL]
}

response = requests.get(WAYBACK_API_ENDPOINT, params=payload)
result = response.json()
result = result[1:]  # get rid of the field name list

for capture in result:
    actual_url = '{wayback}/{timestamp}/{url}'.format(wayback=WAYBACK_URL_ENDPOINT,
                                                      timestamp=capture[0],
                                                      url=capture[1])

    output_fn = os.path.join(IMAGE_OUTPUT_DIRECTORY, '{timestamp}.png'.format(timestamp=capture[0]))
    if not os.path.exists(output_fn):
        cmd = 'curl http://localhost:3000/?url={url} > {output_fn}'.format(url=actual_url,
                                                                           output_fn=output_fn)
        call(cmd, shell=True)

cmd = 'convert -delay {lapse_speed} staging/images/*.png waybacklapse.gif'.format(lapse_speed=LAPSE_SPEED)
call(cmd, shell=True)
