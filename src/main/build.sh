#!/usr/bin/env nix-shell
#!nix-shell -i bash shell.nix
# Default canonical tag
docker build -t "${DOCKERHUB_REPO}/${PROJECT_NAME}:${VERSION}" \
  -f geonode/scripts/spcgeonode/django/Dockerfile \
  geonode
