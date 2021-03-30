#!/usr/bin/env nix-shell
#!nix-shell -i python3 ../shell.nix
"""
Overlay phase

Overlay phase merged and combine all files in the overlay directory
then copy it into the build folder
"""
import os
import shutil
import subprocess
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
            source_targetpath = os.path.join(overlay['overlay'], s)
            if os.path.islink(source_targetpath):
                try:
                    os.remove(full_targetpath)
                except BaseException:
                    pass
                shutil.copy(source_targetpath, full_targetpath, follow_symlinks=False)
            else:
                os.makedirs(full_targetpath, exist_ok=True)
    # Copy over files from sources
    for overlay in sorted_overlays['file_sources']:
        overlay_rootpath = overlay['overlay']
        for s in overlay['sources']:
            full_targetpath = os.path.join(build_dir, s)
            full_sourcepath = os.path.join(overlay_rootpath, s)
            try:
                os.remove(full_targetpath)
            except BaseException:
                pass

            try:
                shutil.copy(
                    full_sourcepath, full_targetpath,
                    follow_symlinks=False)
            except SameFileError:
                pass

    # run overlay hooks (from the build dir)
    # pass on the template file lists as json, to the stdin
    try:
        subprocess.run(
            ["bash", "-c", ".overlay-hooks/overlay.sh"],
            cwd=build_dir)
    except:
        pass


if __name__ == '__main__':
    main()
