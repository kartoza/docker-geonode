{# 
This Docker image recipes is to build standard prod Image.

GeoNode docker images don't use Multistage recipe.
So we construct it from them.
#}

{% include 'geonode/scripts/spcgeonode/django/Dockerfile' %}

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

ENTRYPOINT [ "/spcgeonode/scripts/spcgeonode/django/docker-entrypoint.sh" ]
CMD [ "uwsgi", "--ini=/uwsgi.conf" ]