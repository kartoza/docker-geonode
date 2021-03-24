#!/usr/bin/env bash

echo "Executing bootstrap hook: $PWD"

ln -sf "${BUILD_DIRECTORY}/.gitignore" "${PROJECT_ROOT}/.gitignore"
ln -sf "${BUILD_DIRECTORY}/.envrc" "${PROJECT_ROOT}/.envrc"
ln -sf "${BUILD_DIRECTORY}/.env" "${PROJECT_ROOT}/.env"
ln -sf "${BUILD_DIRECTORY}/Makefile" "${PROJECT_ROOT}/Makefile"
ln -sf "${BUILD_DIRECTORY}/default.nix" "${PROJECT_ROOT}/shell.nix"
