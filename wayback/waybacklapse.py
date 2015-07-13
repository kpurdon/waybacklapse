import os
from multiprocessing import Pool
from subprocess import call

import click

from wayback import Wayback


RASTERIZE_SCRIPT = os.environ['rasterize']
WIDTH = 1024
RATIO = 4 / 3
HEIGHT = int(WIDTH / RATIO)


def capture_url(item):

    output_fn = os.path.join('/output', '{0}.png'.format(item[0]))
    print('Attemting to download: {0}'.format(item[1]))
    cmd = 'phantomjs {rast} "{url}" {out} "{w}px*{h}px"'
    cmd = cmd.format(rast=RASTERIZE_SCRIPT, url=item[1], out=output_fn, w=WIDTH, h=HEIGHT)
    call(cmd, shell=True)


@click.command()
@click.argument('url')
@click.option('-b', '--beginning')
@click.option('-e', '--end')
def cli(url, beginning, end):
    """
    Waybacklapse:\n
    \t-b/-beginning: YYYY to begin search\n
    \t-e/-end: YYYY to end search
    """

    items = Wayback(url, beginning, end).search()

    with Pool(processes=10) as pool:  # not sure how to correctly set this
        pool.map(capture_url, items)

if __name__ == '__main__':
    cli()
