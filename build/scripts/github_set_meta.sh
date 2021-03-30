#!/usr/bin/env bash
# Used to set build meta for Github Action


if [[ -n "$GITHUB_ACTIONS" ]]; then
  echo "Github Actions detected."
  echo "Set output variable meta."
  echo "::set-output name=DOCKERHUB_REPO::${DOCKERHUB_REPO}"
  echo "::set-output name=VERSION::${VERSION}"
  echo "::set-output name=MAIN_APP_VERSION::${MAIN_APP_VERSION}"
  echo "::set-output name=COMPONENT_VERSION::${COMPONENT_VERSION}"
  echo "::set-output name=APP_VERSION::${APP_VERSION}"
  echo "::set-output name=MAIN_PROJECT_NAME::${MAIN_PROJECT_NAME}"
  echo "::set-output name=PROJECT_NAME::${PROJECT_NAME}"

  # Generate Full Image Tag for canonical tag
  if [[ "${GITHUB_REF}" =~ "^refs/heads/tag" ]]; then
    echo "::set-output name=CANONICAL_IMAGE_TAG::${CANONICAL_IMAGE_TAG}"
  else
    echo "::set-output name=CANONICAL_IMAGE_TAG::"
  fi

  # Generate Full Image Tag for latest in the branch
  echo "::set-output name=LATEST_IMAGE_TAG::${LATEST_IMAGE_TAG}"
  # Generate Full Image Tag for major version
  echo "::set-output name=MAJOR_IMAGE_TAG::${MAJOR_IMAGE_TAG}"

  # Same as above, but for the variants
  # Generate Full Image Tag for canonical tag
  if [[ "${GITHUB_REF}" =~ "^refs/heads/tag" ]]; then
    echo "::set-output name=CANONICAL_VARIANT_IMAGE_TAG::${CANONICAL_VARIANT_IMAGE_TAG}"
  else
    echo "::set-output name=CANONICAL_VARIANT_IMAGE_TAG::"
  fi

  # Generate Full Image Tag for latest in the branch
  echo "::set-output name=LATEST_VARIANT_IMAGE_TAG::${LATEST_VARIANT_IMAGE_TAG}"
  # Generate Full Image Tag for major version
  echo "::set-output name=MAJOR_VARIANT_IMAGE_TAG::${MAJOR_VARIANT_IMAGE_TAG}"
fi
