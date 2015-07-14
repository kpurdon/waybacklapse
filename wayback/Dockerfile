FROM python:3.4-onbuild

MAINTAINER Kyle W. Purdon

# install phantomjs
ENV PHANTOMJS_VERSION 1.9.8
RUN wget --no-check-certificate -q -O - https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 | tar xjC /opt
RUN ln -s /opt/phantomjs-$PHANTOMJS_VERSION-linux-x86_64/bin/phantomjs /usr/bin/phantomjs
ENV rasterize /opt/phantomjs-$PHANTOMJS_VERSION-linux-x86_64/examples/rasterize.js

# install imagemagick
RUN apt-get update && apt-get install -y imagemagick
