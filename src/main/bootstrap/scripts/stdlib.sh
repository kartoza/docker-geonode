#!/usr/bin/env bash

## Collection of bash function shared between bootstrap scripts.

function sort_overlays {
  # arguments:
  # $1: overlay directory
  overlay_dir=$1
  dirs=$(ls "$overlay_dir")
}
