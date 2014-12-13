waybacklapse
==========

A quick python project which can be run from the command line and will generate a time-lapse of a given website using the WayBack Machine.

# Installation

This tool currently has dependencies on external projects and is only tested on a mac.

## Install Dependencies

```
brew install imagemagick
brew install phantomjs
git clone https://github.com/fzaninotto/screenshot-as-a-service.git
cd screenshot-as-a-service
git checkout -t v1.1.0
npm install
```

## Install My Source
```
git clone https://github.com/kpurdon/waybacklapse.git
cd waybacklapse
virtualenv .waybacklapse
. .waybacklapse/bin/activate
pip install click requests
```

# Running The Tool

## Start the screenshot-as-a-service node app

```
cd screenshot-as-a-service && node app
```

## Run waybacklapse.py

### Example:

The following will generate a GIF of google.com from 2000-2004 at a yearly interval at a medium lapse speed. The screenshot images will be stored in ./output/{currentdatetime}/ and the GIF will be in ./ouput/{currentdatetime}/timelapse/{somefn}.gif

TODO: More documentation on command options.
TODO: Defaults on the command options. (None for now)

```
cd waybacklapse
. .waybacklapse/bin/activate
python waybacklapse.py google.com 2000 2004 output/ 75 yearly
```
