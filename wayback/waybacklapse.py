import os
from multiprocessing import Pool
from subprocess import call
from datetime import datetime as dt

import click

from wayback import Wayback


TMP_OUTPUT_DIR = '/images'
GIF_OUTPUT_DIR = '/output'
RASTERIZE_SCRIPT = os.environ['rasterize']


def capture_url(item):
    output_fn = os.path.join('/images', '{0}.png'.format(item[0]))
    print('Attemting to download: {0}'.format(item[1]))
    cmd = 'phantomjs {rast} "{url}" {out}'
    cmd = cmd.format(rast=RASTERIZE_SCRIPT, url=item[1], out=output_fn)
    call(cmd, shell=True)


def create_output_fn(url):
    keepcharacters = ('.', '_')
    safe_fn = ''.join(c for c in url if c.isalnum() or c in keepcharacters).rstrip()
    output_fn = os.path.join(GIF_OUTPUT_DIR, '{fn}.gif'.format(fn=safe_fn))
    return output_fn


@click.command()
@click.option('-u', '--url', default='google.com',
              prompt='What URL would you like to create a timelapse of (ex. google.com)')
@click.option('-b', '--beginning', default='1996',
              prompt='What year (YYYY) would you like your timelapse to start')
@click.option('-e', '--end', default=dt.now().strftime('%Y'),
              prompt='What year (YYYY) would you like your timelapse to end')
@click.option('-c', '--collapse', type=click.Choice(['4', '6']), default='4',
              prompt='Do you want monthly (6) or yearly (4) images')
@click.option('-s', '--speed', default=50,
              prompt='What speed would you like your timelapse (100=slow|25=fast)')
@click.option('-l', '--limit', default=100,
              prompt='What is the max number of images you want')
@click.option('-v', '--verbose', is_flag=True)
def cli(url, beginning, end, collapse, speed, limit, verbose):
    """
    Generate a GIF of a given website over a given time range.
    """

    items = Wayback(url, beginning, end, collapse).search()
    items = items[:limit]

    # not sure how to correctly set this, trial and error...
    with Pool(processes=12) as pool:
        pool.map(capture_url, items)

    output_fn = create_output_fn(url)

    cmd = 'convert'
    if verbose:
        cmd += ' -verbose'
    cmd += ' -delay {speed} {images} {gif}'
    cmd = cmd.format(speed=speed, images=os.path.join(TMP_OUTPUT_DIR, '*.png'), gif=output_fn)
    print(cmd)
    call(cmd, shell=True)


if __name__ == '__main__':
    cli()
