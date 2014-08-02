#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM ubuntu:trusty
MAINTAINER Tim Sutton<tim@linfiniti.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe" > /etc/apt/sources.list
RUN apt-get update -y

#-------------Application Specific Stuff ----------------------------------------------------

RUN apt-get -y -f install --no-install-recommends openjdk-7-jdk; update-alternatives –config java
RUN apt-get install -q -y python python-pip python-dev python-lxml gdal-bin

RUN pip install geonode

RUN django-admin.py startproject project_name --template=https://github.com/GeoNode/geonode-project/archive/master.zip -epy,rst

WORKDIR project_name
RUN paver setup
EXPOSE 8000
CMD paver start -b 0.0.0.0:8000

