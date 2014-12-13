import os
import sys
import requests
from subprocess import call
import datetime as dt

import click


WAYBACK_SEARCH_API = 'http://web.archive.org/cdx/search/cdx'
WAYBACK_IMAGE_API = 'http://web.archive.org/web'


def create_payload(url, start_year, stop_year, timelapse_level):

    collapse_options = {'yearly': 'timestamp:4', 'monthly': 'timestamp:6'}
    collapse = collapse_options[timelapse_level]

    payload = {
        'url': url,
        'output': 'json',
        'fl': 'timestamp,original',
        'from': start_year,
        'to': stop_year,
        'collapse': collapse
    }

    return payload


def get_captures_list(payload):

    response = requests.get(WAYBACK_SEARCH_API, params=payload)
    if response.status_code == 503:
        sys.tracebacklimit = 0
        raise Exception(('The Wayback Machine API is down.'
                         'Check http://web.archive.org/cdx/search/cdx for details.'))

    captures = response.json()
    captures = captures[1:]  # remove the field names record

    return captures


def construct_capture_urls(captures):

    url_format = '{wayback}/{timestamp}/{url}'
    capture_urls = [
        (capture[0],
         url_format.format(wayback=WAYBACK_IMAGE_API,
                           timestamp=capture[0],
                           url=capture[1]))
        for capture in captures]

    return capture_urls


def create_output_dir(output_dir):
    output_dir_sub = os.path.join(output_dir, dt.datetime.now().strftime('%Y%m%d%H%m%s'))
    if not os.path.exists(os.path.join(output_dir_sub, 'timelapse')):
        os.makedirs(os.path.join(output_dir_sub, 'timelapse'))

    return output_dir_sub


def get_images(output_dir, capture_urls, url):

    try:
        for timestamp, capture_url in capture_urls:

            output_fn = os.path.join(output_dir,
                                     '{url}_{timestamp}.png'.format(url=url, timestamp=timestamp))

            print 'Capturing {url} ...'.format(url=capture_url)

            # node screenshot-as-a-service must be running!
            cmd = 'curl --silent http://localhost:3000/?url={url} > {output_fn}'
            cmd = cmd.format(url=capture_url, output_fn=output_fn)

            print 'Attemting to download: {output_fn}'.format(output_fn=output_fn)
            call(cmd, shell=True)

    except:
        raise Exception('Getting image failed. Is screenshot-as-a-service running?')


def convert_images(output_dir, url, timelapse_speed):

    try:
        image_search_string = os.path.join(output_dir, '*.png')
        output_fn = os.path.join(output_dir, 'timelapse',
                                 '{url}.gif'.format(url=url))

        # imagemagick must be installed!
        cmd = 'convert -delay {speed} {images} {gif}'
        cmd = cmd.format(speed=timelapse_speed,
                         images=image_search_string,
                         gif=output_fn)

        print 'Generating GIF ({cmd})'.format(cmd=cmd)
        call(cmd, shell=True)

    except:
        raise Exception('Converting images to GIF failed. Is imagemagick installed?')


@click.command()
@click.argument('url')
@click.argument('start_year')
@click.argument('stop_year')
@click.argument('output_dir')
@click.argument('timelapse_speed')
@click.argument('timelapse_level')
def waybacklapse(url, start_year, stop_year,
                 output_dir, timelapse_speed,
                 timelapse_level):

    payload = create_payload(url, start_year, stop_year,
                             timelapse_level)
    captures = get_captures_list(payload)
    capture_urls = construct_capture_urls(captures)

    output_dir = create_output_dir(output_dir)
    get_images(output_dir, capture_urls, url)
    convert_images(output_dir, url, timelapse_speed)


if __name__ == '__main__':
    waybacklapse()
