# Kartoza's GeoNode Docker Builder

Docs for GeoNode image builder for this branch.

Source GeoNode Git URL: ![Source GeoNode Git URL](https://img.shields.io/badge/source-{{ "" | from_env('GEONODE_SOURCE_URL') | e }}-blue)

Docker Image tag: ![Docker Image Tag](https://img.shields.io/badge/docker%20image%20tag-{{ "" | from_env('LATEST_IMAGE_TAG') | e }}-blue)

Main App Version (GeoNode): ![Main App Version](https://img.shields.io/badge/main%20app%20version-{{ "" | from_env('MAIN_APP_VERSION') | e }}-blue)

# How to use

This image uses SPCGeoNode image variant.

The recipe to use such docker images is described in this [directory](geonode/scripts/spcgeonode). Look at the `docker-compose.yml` and `docker-compose.override.yml` recipe there.

Simply replace the docker image for GeoNode to use this tagged image. Like this:

```yaml
x-common-django:
  &default-common-django
  image: {{ "" | from_env('LATEST_IMAGE_TAG') }}
```

# Development Guide

For development guideline, refer to [this doc](docs/DEVELOPMENT.md)