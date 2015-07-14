import os
from multiprocessing import Pool
from subprocess import call

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


@click.command()
@click.option('-u', '--url',
              prompt='What URL would you like to create a timelapse of (ex. google.com)')
@click.option('-b', '--beginning',
              prompt='What year (YYYY) would you like your timelapse to start')
@click.option('-e', '--end',
              prompt='What year (YYYY) would you like your timelapse to end')
@click.option('-c', '--collapse', type=click.Choice(['4', '6']),
              prompt='Do you want monthly (6) or yearly (4) images')
@click.option('-s', '--speed',
              prompt='What speed would you like your timelapse (100=slow|25=fast)')
def cli(url, beginning, end, collapse, speed):
    """
    Generate a GIF of a given website over a given time range.
    """

    items = Wayback(url, beginning, end, collapse).search()

    with Pool(processes=10) as pool:  # not sure how to correctly set this
        pool.map(capture_url, items)

    output_fn = os.path.join(GIF_OUTPUT_DIR, 'waybacklapse.gif')
    cmd = 'convert -verbose -delay {speed} {images} {gif}'
    cmd = cmd.format(speed=speed, images=os.path.join(TMP_OUTPUT_DIR, '*.png'), gif=output_fn)
    print(cmd)
    call(cmd, shell=True)


if __name__ == '__main__':
    cli()
