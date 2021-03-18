#!/usr/bin/env nix-shell
#!nix-shell -i python3 ../shell.nix
"""
Bootstrap phase

Bootstrap phase should be an idempotent phase.
It can be run multiple times while producing the same state.

Initial overlay creation are started by executing bootstrap phase.
The project directory might only contains the bootstrap package.

From the root of the bootstrap package we should be able to run
`make bootstrap` or equivalent to run this script.
The script will then populate needed project structure, including but not
limited to:
- Final build directory
- Dependency manager related files (currently on top of nix)
- Environment manager related files (currently on top of direnv)
"""
import os
import shutil
import subprocess
import sys


def main():
    # Make sure final build directory exists
    overlay_dir = sys.argv[1]
    build_dir = sys.argv[2]
    bootstrap_dir = sys.argv[3]
    project_dir = sys.argv[4]
    os.makedirs(build_dir, exist_ok=True)

    # Copy over minimum dependency manager to bootstrap entire project build
    # overlay_dir should refer to source of the overlay_dir
    # bootstrap_dir should refer to "specific" bootstrap package directory
    # where the script is initiated.
    # bootstrap_dir might get changed later if the final project structure is
    # constructed so that it will refer to the bootstrap package inside the
    # bootstrap_dir directory instead of manually specifying the bootstrap
    # package
    needed_files = [
        '.envrc',
        '.env',
        '.local.env',
        '.local.envrc',
        'default.nix',
        'shell.nix',
        'Makefile'
    ]
    # copy bootstrap package if it is not being run from project root
    if not os.getcwd() == project_dir:
        target_full_path = os.path.join(build_dir, os.path.basename(
            bootstrap_dir))
        try:
            shutil.rmtree(target_full_path)
        except:
            pass
        shutil.copytree(
            bootstrap_dir, target_full_path,
            symlinks=True,
            ignore_dangling_symlinks=True)

    # Link over minimum dependency manager to project root
    for f in needed_files:
        source_full_path = os.path.join(bootstrap_dir, f)
        target_full_path = os.path.join(project_dir, f)
        if os.path.exists(source_full_path):
            if os.path.exists(target_full_path):
                os.remove(target_full_path)
            os.symlink(source_full_path, target_full_path)

    # run bootstrap hooks (from the build dir or bootstrap dir)
    try:
        if not os.getcwd() == project_dir:
            subprocess.run(
                ["bash", "-c", ".overlay-hooks/bootstrap.sh"],
                cwd=bootstrap_dir)
        else:
            subprocess.run(
                ["bash", "-c", ".overlay-hooks/bootstrap.sh"],
                cwd=build_dir)
    except:
        pass

    # run bootstrap again, only if the current phase is not run from the
    # project root
    if not os.getcwd() == project_dir:
        subprocess.run(["make", "bootstrap"], cwd=project_dir)


if __name__ == '__main__':
    main()
