#!/usr/bin/env nix-shell
#!nix-shell -i bash shell.nix
# Default canonical tag
set -eux

if [[ -n "${IMAGE_VARIANT}" ]]; then
  docker build -t "${CANONICAL_IMAGE_TAG}" \
    -f variants/${IMAGE_VARIANT}/${IMAGE_VARIANT}.Dockerfile \
    --target ${IMAGE_VARIANT} \
    .
else
  docker build -t "${CANONICAL_IMAGE_TAG}" \
    -f variants/Dockerfile \
    .
fi
