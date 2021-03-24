#!/usr/bin/env bash
# Used to set build meta for Github Action


if [[ -n "$GITHUB_ACTIONS" ]]; then
  echo "::set-output name=DOCKERHUB_REPO::${DOCKERHUB_REPO}"
  echo "::set-output name=VERSION::${VERSION}"
  echo "::set-output name=MAIN_APP_VERSION::${MAIN_APP_VERSION}"
  echo "::set-output name=COMPONENT_VERSION::${COMPONENT_VERSION}"
  echo "::set-output name=APP_VERSION::${APP_VERSION}"
  echo "::set-output name=MAIN_PROJECT_NAME::${MAIN_PROJECT_NAME}"
  echo "::set-output name=PROJECT_NAME::${PROJECT_NAME}"

  # Generate Full Image Tag for canonical tag
  if [[ "${GITHUB_REF}" =~ "^refs/head/tag" ]]; then
    echo "::set-output name=CANONICAL_IMAGE_TAG::${DOCKERHUB_REPO}/${PROJECT_NAME}:${APP_VERSION}/${VERSION}"
  else
    echo "::set-output name=CANONICAL_IMAGE_TAG::"
  fi

  # Generate Full Image Tag for latest in the branch
  if [[ "${GITHUB_REF}" == "refs/head/main" ]]; then
    echo "::set-output name=LATEST_IMAGE_TAG::${DOCKERHUB_REPO}/${PROJECT_NAME}:stable"
  elif [[ "${GITHUB_REF}" == "refs/head/develop" ]]; then
    echo "::set-output name=LATEST_IMAGE_TAG::${DOCKERHUB_REPO}/${PROJECT_NAME}:latest"
  else
    echo "::set-output name=LATEST_IMAGE_TAG::${DOCKERHUB_REPO}/${PROJECT_NAME}:${MAIN_PROJECT_NAME}/latest"
  fi
  # Generate Full Image Tag for major version
  echo "::set-output name=MAJOR_IMAGE_TAG::${DOCKERHUB_REPO}/${PROJECT_NAME}:${APP_VERSION}/latest"
fi
