waybacklapse
==========

A tool for creating a timelapse from the Wayback Machine.

# Installation

This tool currently has dependencies on external projects and is only tested on MacOS X.

## Install Dependencies

```
brew install imagemagick
brew install phantomjs
git clone https://github.com/fzaninotto/screenshot-as-a-service.git
cd screenshot-as-a-service
git checkout -t v1.1.0
npm install
```

## Install WAYBACKLAPSE (From PyPi)
```
pip install waybacklapse
```

## Install WAYBACKLAPSE (From Source)
```
git clone https://github.com/kpurdon/waybacklapse.git
cd waybacklapse
python setup.py install
```

# Running The Tool

## Start the screenshot-as-a-service node app

```
cd screenshot-as-a-service && node app
```

## Run waybacklapse

For help:
```
waybacklapse --help
```

To run simply enter ```waybacklapse``` at the command line and follow the prompts.
