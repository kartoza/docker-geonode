#!/usr/bin/env bash
# input are given via stdin : <&0
# treat it as a file
# example:
# cat <&0

# Input is a json array like this:
#[
#  {
#    'template': <template-name>
#    'output': <destination-output-name>
#  }
#]

# We are not going to use the input of the scripts.
# We are going to generate build variants from the environment variable toggle
if [[ -n "${IMAGE_VARIANT}" ]]; then
    if [[ -f "${BUILD_DIRECTORY}/variants/${IMAGE_VARIANT}/prepare.sh" ]]; then
        set -eux
        bash "${BUILD_DIRECTORY}/variants/${IMAGE_VARIANT}/prepare.sh"
        set +eux
    fi
fi