# waybacklapse

This is a rewrite of the original waybacklapse using docker and phantomjs directly. It eliminates the need for the screenshot-as-a-service node application. You can still get the original version from pip and can checkout the source using the following command:

* `git clone -b v1.0.1 git@github.com:kpurdon/waybacklapse.git`

You can view the original README [here](https://github.com/kpurdon/waybacklapse/tree/v1.0.1).

## Getting Started

* Have [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) working.

### Quick Method

Requires Python3 on your system.

* `pip install invoke` or `conda install invoke`
* `invoke runner` which will build/start the docker container and run the command-line application. Output will be generated in ./output.

### Detailed Method

* Build the image: `docker-compose build`
* Start the container: `docker-compose up`

To generate a GIF in ./output run: `docker-compose run wayback python3 /usr/src/app/waybacklapse.py`. You will be prompted for inputs. If you want to specify these values (not answering prompts) you can use the flag options shown by `--help`.

## Developing

* Create a virtualenv/conda-env and activate it
* `pip install invoke`
* `invoke test`
* `invoke`
