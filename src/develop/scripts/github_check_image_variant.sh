#!/usr/bin/env bash
# Used to set build meta for Github Action


if [[ -n "$GITHUB_ACTIONS" ]]; then
  echo "Github Actions detected."
  echo "Set output build variant."

  if [[ -d "${BUILD_DIRECTORY}/variants/${IMAGE_VARIANT}" ]]; then
    echo "Image Variant overrides recipe found: ${IMAGE_VARIANT}"
    echo "::set-output name=IS_VARIANT_EXISTS::1"
  fi
fi
