#!/usr/bin/env bash
echo "Running initial bootstrap."
direnv exec . bash '-c' 'echo "Parameters: python -m bootstrap ${OVERLAY_DIRECTORY} ${BUILD_DIRECTORY} ${BOOTSTRAP_DIRECTORY} ${PROJECT_ROOT}"'
direnv exec . nix-shell '--run' 'python -m bootstrap ${OVERLAY_DIRECTORY} ${BUILD_DIRECTORY} ${BOOTSTRAP_DIRECTORY} ${PROJECT_ROOT}'
