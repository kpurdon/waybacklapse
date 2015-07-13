# waybacklapse

This is a rewrite of the original waybacklapse using docker and phantomjs directly. It eliminates the need to the screenshot-as-a-service node application.

## Getting Started

* Build the image: `docker-compose build`

To generate images in ./output (one for each year found for the given url)

* Run: `docker-compose run wayback python3 /usr/src/app/waybacklapse.py -b 2010 -e 2015 https://www.google.com`
