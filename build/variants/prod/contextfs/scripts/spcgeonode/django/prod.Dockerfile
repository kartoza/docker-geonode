

# TODO : use python:2.7.13-alpine3.6 to make this lighter ( it is what we use for letsencryipt as well)
# But it seems it's not possible for now because alpine only has geos 3.6 which is not supported by django 1.8
# (probably because of https://code.djangoproject.com/ticket/28441)

FROM python:3.7-slim-stretch

# Install system dependencies
RUN echo "Updating apt-get" && \
    apt-get update && \
    echo "Installing build dependencies" && \
    apt-get install -y gcc make libc-dev musl-dev libpcre3 libpcre3-dev g++ git && \
    echo "Installing Pillow dependencies" && \
    # RUN apt-get install -y NOTHING ?? It was probably added in other packages... ALPINE needed jpeg-dev zlib-dev && \
    echo "Installing GDAL dependencies" && \
    apt-get install -y libgeos-dev libgdal-dev && \
    echo "Installing Psycopg2 dependencies" && \
    # RUN apt-get install -y NOTHING ?? It was probably added in other packages... ALPINE needed postgresql-dev && \
    echo "Installing other dependencies" && \
    apt-get install -y libxml2-dev libxslt-dev && \
    echo "Installing GeoIP dependencies" && \
    apt-get install -y geoip-bin geoip-database && \
    echo "Installing healthceck dependencies" && \
    apt-get install -y curl && \
    echo "Activate memcached" && \
    apt-get update && apt-get install -y memcached && \
    pip install pylibmc  && pip install sherlock && \
    echo "Python server" && \
    pip install uwsgi && \
    echo "Removing build dependencies and cleaning up" && \
    # TODO : cleanup apt-get with something like apt-get -y --purge autoremove gcc make libc-dev musl-dev libpcre3 libpcre3-dev g++ && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf ~/.cache/pip

# Install python dependencies
RUN echo "GeoNode python dependencies"

# Install geonode dependencies
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

# Install pygdal (after requirements https://github.com/GeoNode/geonode/pull/4599)
RUN pip install pygdal==$(gdal-config --version).*

# Install geonode
RUN mkdir /spcgeonode
WORKDIR /spcgeonode/
ADD . /spcgeonode/
RUN pip install -e . --upgrade
RUN chmod +x scripts/spcgeonode/django/docker-entrypoint.sh

# Export ports
EXPOSE 8000

# We provide no command or entrypoint as this image can be used to serve the django project or run celery tasks

# Redeclare and compactify layers to use Multistage targeting
FROM scratch as prod

COPY --from=0 / /
# Not efficient way to extend the base image because the original image don't use Multistage recipe.
# But there's no other way for now

# Include uwsgi config

LABEL com.kartoza.docker.image.app_version="${APP_VERSION}" \
    com.kartoza.docker.image.maintainers="rizky@kartoza.com,lana.pcfre@gmail.com,maul@hey.com" \
    com.kartoza.docker.image.project_name="${PROJECT_NAME}" \
    com.kartoza.docker.image.variants="prod"

ADD rootfs/uwsgi.conf /uwsgi.conf
WORKDIR /spcgeonode
ENTRYPOINT [ "/spcgeonode/scripts/spcgeonode/django/docker-entrypoint.sh" ]
CMD [ "uwsgi", "--ini=/uwsgi.conf" ]