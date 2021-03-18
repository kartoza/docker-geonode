#!/usr/bin/env nix-shell
#!nix-shell -i python3 ../shell.nix
"""
Overlay phase

Overlay phase merged and combine all files in the overlay directory
then copy it into the build folder
"""
import os
import shutil
import sys
from shutil import SameFileError

from bootstrap import stdlib


def main():
    overlay_dir = sys.argv[1]
    build_dir = sys.argv[2]
    sorted_overlays = stdlib.overlays_merge(overlay_dir)
    # Create build directory if not exists
    os.makedirs(build_dir, exist_ok=True)
    for overlay in sorted_overlays['dir_sources']:
        for s in overlay['sources']:
            full_targetpath = os.path.join(build_dir, s)
            os.makedirs(full_targetpath, exist_ok=True)
    # Copy over files from sources
    for overlay in sorted_overlays['file_sources']:
        overlay_rootpath = overlay['overlay']
        for s in overlay['sources']:
            full_targetpath = os.path.join(build_dir, s)
            full_sourcepath = os.path.join(overlay_rootpath, s)
            try:
                shutil.copy(
                    full_sourcepath, full_targetpath,
                    follow_symlinks=False)
            except SameFileError:
                pass


if __name__ == '__main__':
    main()
