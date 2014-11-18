waybacklapse
==========

An exploratory project to create a timelapse from the wayback machine internet achive.


It'll be ugly, not well (if at all) tested until I decide this is viable.

# set-up

## install stuff

```
brew install imagemagick
brew install phantomjs
git clone https://github.com/fzaninotto/screenshot-as-a-service.git -t v1.1.0
cd screenshot-as-a-service && npm install
node app
```

## download my thing
```
git clone https://github.com/kpurdon/waybacklapse.git
cd waybacklapse
[EDIT lapsify.py for years, timescale, URL, ...]
python lapsify.py
```

## it does it's thing

lapsify will get a bunch of images in staging/images/*

and!!!! it will create waybacklapse.gif in the root.

## beware

there is no cleanup. do this
```
rm -rf staging/images/*
rm waybacklapse.gif
```
