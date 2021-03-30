# Kartoza's GeoNode Docker Builder

Docs for GeoNode image builder for this branch.

Source URLs: 

![geonode](https://img.shields.io/badge/source-https://github.com/GeoNode/geonode/tree/5d796a6f094bd6474bbd72a269235257f9cbab34-blue)

Docker image tags (latest): 

![Docker Image Tag](https://img.shields.io/badge/docker%20image%20tag-kartoza/geonode%3Astable-blue)

Main App Version (GeoNode): ![Main App Version](https://img.shields.io/badge/main%20app%20version-3.1-blue)

# How to use

This image uses SPCGeoNode image variant.

The recipe to use such docker images is described in this [directory](/src/main/geonode/scripts/spcgeonode). Look at the `docker-compose.yml` and `docker-compose.override.yml` recipe there.

Simply replace the docker image for GeoNode to use this tagged image. Like this:

```yaml
x-common-django:
  &default-common-django
  image: kartoza/geonode:stable
```

# Development Guide

For development guideline, refer to [this doc](docs/DEVELOPMENT.md)