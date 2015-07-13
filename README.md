# waybacklapse

This is a rewrite of the original waybacklapse using docker and phantomjs directly. It eliminates the need for the screenshot-as-a-service node application.

## Getting Started

* Build the image: `docker-compose build`

To generate a GIF in ./output run: `docker-compose run wayback python3 /usr/src/app/waybacklapse.py`. You will be prompted for an input URL, start and stop date, and output GIF speed. If you want to specify these values (not answering prompts) you can use the flag options shown by `--help`.
