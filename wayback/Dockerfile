FROM python:3.4.3

MAINTAINER Kyle W. Purdon

# install phantomjs
ENV PHANTOMJS_VERSION 2.1.1
RUN wget --no-check-certificate -q -O - https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 | tar xjC /opt
RUN ln -s /opt/phantomjs-$PHANTOMJS_VERSION-linux-x86_64/bin/phantomjs /usr/bin/phantomjs

# install imagemagick
RUN apt-get update && apt-get install -y imagemagick

# make application directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# install python requirements
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# copy in the application source
COPY . /usr/src/app
