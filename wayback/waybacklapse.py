import os
import time
import contextlib
from multiprocessing import Pool
from itertools import repeat
from subprocess import call
from datetime import datetime as dt

import click
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import wayback


TMP_OUTPUT_DIR = '/images'
GIF_OUTPUT_DIR = '/output'


class closing(contextlib.closing):

    def __exit__(self, *exc_info):
        self.thing.quit()


def capture_url(item, width, height, allow_redirects):

    output_fn = os.path.join(TMP_OUTPUT_DIR, '{0}.png'.format(item[0]))
    print('Attemting to capture: {0}'.format(item[1]))

    with closing(webdriver.PhantomJS()) as driver:
        driver.set_window_size(width, height)
        driver.get(item[1])
        try:
            redirect_link = driver.find_element_by_link_text('Impatient?')
            redirected = True  # redirect was found (redirect if allowed)
            if allow_redirects:
                while True:  # continue until all redirects are resolved
                    print('Redirected to: {0}'.format(redirect_link.get_attribute('href')))
                    redirect_link.click()
        except NoSuchElementException:
            redirected = False  # no redirect was found
        except StaleElementReferenceException:
            redirected = True  # redirect resolved before the "impatient" link was clicked
        finally:
            if not redirected or allow_redirects:  # only capture redirect if redirects are allowed
                driver.get_screenshot_as_file(output_fn)
                call('mogrify -crop {0}x{1}+0+0 {2}'.format(width, height, output_fn), shell=True)


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
@click.option('-w', '--width', default=1280,
              prompt='What output width (in px) do you want')
@click.option('-h', '--height', default=720,
              prompt='What output height (in px) do you want')
@click.option('-v', '--verbose', is_flag=True, default=False, prompt='Do you want verbose output')
@click.option('-a', '--allow_redirects', is_flag=True, default=False,
              prompt='Do you want to allow redirects (experimental)')
def cli(url, beginning, end, collapse, speed, limit, width, height, verbose, allow_redirects):
    """
    Generate a GIF of a given website over a given time range.
    """

    items = wayback.Wayback(url, limit, beginning, end, collapse).search()
    
    if not os.path.exists(TMP_OUTPUT_DIR):
        os.mkdir(TMP_OUTPUT_DIR)

    # not sure how to correctly set this, trial and error...
    with Pool(processes=12) as pool:
        pool.starmap(capture_url, zip(items, repeat(width), repeat(height),
                                      repeat(allow_redirects)))

    output_fn = create_output_fn(url)

    cmd = 'convert'
    cmd += ' -delay {0}'.format(speed)
    cmd += ' {0}'.format(os.path.join(TMP_OUTPUT_DIR, '*.png'))
    if verbose:
        cmd += ' -verbose'
    cmd += ' -background "rgb(255,255,255)"'
    cmd += ' -alpha Remove'
    cmd += ' {0}'.format(output_fn)
    print(cmd)
    call(cmd, shell=True)


if __name__ == '__main__':
    cli()
