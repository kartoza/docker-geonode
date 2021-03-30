#!/usr/bin/env nix-shell
#!nix-shell -i bash shell.nix
# Default canonical tag
set -eux

if [[ -n "${IMAGE_VARIANT}" ]]; then
  docker build -t "${CANONICAL_IMAGE_TAG}" \
    -f geonode/scripts/spcgeonode/django/${IMAGE_VARIANT}.Dockerfile \
    --target ${IMAGE_VARIANT} \
    geonode
else
  docker build -t "${CANONICAL_IMAGE_TAG}" \
    -f geonode/scripts/spcgeonode/django/Dockerfile \
    geonode
fi
